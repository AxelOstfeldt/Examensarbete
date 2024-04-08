-- AdjacentResiduals

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all; -- Import the numeric_std package for signed type	

entity AdjacentResiduals is

   port (
      clk            : in std_logic;
      reset          : in std_logic;
      mic            : in unsigned(5 downto 0);
      original_value : in std_logic_vector(23 downto 0);
      residual       : out std_logic_vector(23 downto 0);
      modResult      : out integer range 0 to 10
   );

end entity;

architecture Behavioral of AdjacentResiduals is

   --Varför kommer inte initial värden med på mina signaler i testbench?
   signal prediction     : signed (23 downto 0);
   signal prediction_row : signed (23 downto 0);
begin
   process (clk)
   begin
      if rising_edge(clk) then

         modResult <= to_integer(mic) mod 8;
         --Check if the current mic value corresponds to the first mic in a row
         if to_integer(mic) mod 8 = 0 then
            --Calculate the residual, 
            --if it is the first mic in the row calculate from the first mic in the previous row
            residual <= std_logic_vector(signed(original_value) - prediction_row);

         else
            --Calculate the residual
            residual <= std_logic_vector(signed(original_value) - prediction);

         end if;

      elsif falling_edge(clk) then
         --Check if the current mic value corresponds to the first mic in a row
         if to_integer(mic) mod 8 = 0 then
            -- if it is the first mic in the row, update first mic in row value
            prediction_row <= signed(original_value);
         end if;
         --update prediction value
         prediction <= signed(original_value);

         if reset = '1' then
            prediction_row <= (others => '0');
            prediction     <= (others => '0');
         end if;

      end if;
   end process;

end Behavioral;