-- Adjacent

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all; -- Import the numeric_std package for signed type	

entity Adjacent is

	port
	( 
		clk : in std_logic;
		
		original_value : out std_logic_vector(23 downto 0);
		recrated_value : out std_logic_vector(23 downto 0)
		);
		
end entity;

architecture Behavioral of Adjacent is

signal current_mic : signed (23 downto 0);
signal prediction_in : signed (23 downto 0) := (others => '0');
signal prediction_in_row : signed (23 downto 0) := (others => '0');
signal prediction_out : signed (23 downto 0) := (others => '0');
signal prediction_out_row : signed (23 downto 0) := (others => '0');
signal current_residual : signed (23 downto 0);
signal residuals : std_logic_Vector(1535 downto 0);
signal input_vector :  std_logic_vector(1535 downto 0) := (others => '0');
signal counter : signed (23 downto 0) := (others => '0');
signal set_input : std_logic := '1';
signal calc_residuals : std_logic := '0';
signal calc_output : std_logic := '0';
signal mic : natural range 0 to 63 := 0; --


begin

	-- Process to assign values to input_vector
	process(clk)
	begin
		if rising_edge(clk) then
		
		
			
			-- if set_input = '1' then the input vector values are set
			if set_input = '1' then
				counter <= counter + "1";
				input_vector((mic + 1) * 24 - 1 downto mic * 24) <= std_logic_vector(counter);
				
				mic <= mic + 1;
				
				-- once mic = 63 all mic values have been set
				-- set_input is then set to '0', mic = 0, and calc_residuals is set to '1'
				if mic = 63 then
					set_input <= '0';
					calc_residuals <= '1';
					mic <= 0;
				end if;
				
			-- if calc_residuals '1' then residual is calculated
			elsif calc_residuals = '1' then
			
				--Current mic is 24 bit value for a specific mic, the for loop loops thorugh all 64 mics
				current_mic <= signed(input_vector((mic + 1) * 24 - 1 downto mic * 24));
				
				
				-- if mic is evenly divideable with 8 a new row of microphones have been reached
				if mic mod 8 = 0 then
					-- calculate the residual by subtracting current mic value with the predicted value
					current_residual <= current_mic - prediction_in_row;
					
					
					--update prediciton
					prediction_in <= current_mic;
					prediction_in_row <= current_mic;
				else
					-- calculate the residual by subtracting current mic value with the predicted value
					current_residual <= current_mic - prediction_in;
				
					--update prediciton
					prediction_in <= current_mic;
				end if;
				
				--Save the current residual at the correct slot in the residuals array
				residuals((mic + 1) * 24 - 1 downto mic * 24) <= std_logic_vector(current_residual);
				
				-- increment mic by 1 to set the next mic
				mic <= mic + 1;
				
				-- once all 63 mics have been set calc_residuals = '0', mic = 0, and calc_output = '1'
				if mic = 63 then
					calc_residuals <= '0';
					calc_output <= '1';
					mic <= 0;
				end if;
				
				
					
			elsif calc_output = '1' then
					
					
				--grab the relevant residual
				current_residual <= signed(residuals((mic + 1) * 24 - 1 downto mic * 24));
				 
				 -- if mic is evenly divideable with 8 a new row of microphones have been reached
				if mic mod 8 = 0 then
					-- calculate the recreated value by adding the predicted value to the current residual
					current_mic <= current_residual + prediction_out_row;
					
					
					--update prediciton
					prediction_out <= current_mic;
					prediction_out_row <= current_mic;
				else
					-- calculate the recreated value by adding the predicted value to the current residual
					current_mic <= current_residual + prediction_out;
					
					
					--update prediciton
					prediction_out <= current_mic;
				end if;
				
				--Save the current mics recreated value at the recrated_value
				recrated_value <= std_logic_vector(current_mic);
				
				--Save the created input values in the original value in order to be able to compare the results
				original_value <= input_vector((mic + 1) * 24 - 1 downto mic * 24);
				
				mic <= mic + 1;
				
				if mic = 63 then
					mic <= 0;
					calc_output <= '0';
					set_input <= '1';
				end if;
				

			end if;
		end if;
	end process;



end Behavioral;