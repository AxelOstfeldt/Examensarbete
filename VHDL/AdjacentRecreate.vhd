-- AdjacentRecreate

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all; -- Import the numeric_std package for signed type	

entity AdjacentRecreate is

   port (
      clk             : in std_logic;
      reset           : in std_logic;
      mic             : in unsigned(5 downto 0);
      residual        : in std_logic_vector(23 downto 0);
      recreated_value : out std_logic_vector(23 downto 0);
      modResult       : out integer range 0 to 10
   );

end entity;

architecture Behavioral of AdjacentRecreate is
   signal previous_value     : signed (23 downto 0);
   signal previous_value_row : signed (23 downto 0);
   signal current_residual   : signed (23 downto 0);
   signal current_mic        : integer range 0 to 63;
begin

   --This process checks if a new value is available
   process (clk)
   begin
      if rising_edge(clk) then
         -- set current mic and current input value
         current_mic      <= to_integer(mic);
         current_residual <= signed(residual);
         modResult        <= to_integer(mic) mod 8;
         --Check if the current mic value corresponds to the first mic in a row
         if to_integer(mic) mod 8 = 0 then
            --Recreate the orginal value by adding the previous mic value to the residual 
            --if it is the first mic in the row calculate from the first mic in the previous row
            recreated_value <= std_logic_vector(signed(residual) + previous_value_row);
            --update previous value with the recreated value
            previous_value <= signed(recreated_value);
            -- if it is the first mic in the row, update first mic in row value
            previous_value_row <= signed(recreated_value);

         else
            --Calculate the residual
            recreated_value <= std_logic_vector(signed(residual) + previous_value_row);
            --update previous value with the recreated value
            previous_value <= signed(recreated_value);

         end if;


         if reset = '1' then
            current_residual   <= (others => '0');
            previous_value     <= (others => '0');
            previous_value_row <= (others => '0');
            current_mic        <= 0;

         end if;
      end if;
   end process;
end Behavioral;