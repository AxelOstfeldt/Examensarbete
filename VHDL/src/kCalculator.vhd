-- kCalculator

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity kCalculator is

   port (
      reset         : in std_logic;
      clk           : in std_logic;
      OriginalValue : in std_logic_vector(23 downto 0);--value in to be encoded
      NewDataIn     : in std_logic;--New data available for input

      ReadyToRecive : out std_logic;
      NewKOut       : out std_logic;--New k-value to be sent
      ErrorOut      : out std_logic;--Send an error signal when error state is reached
      k_value       : out std_logic_vector(4 downto 0)--k-value between 0 and 31

   );

end entity;

architecture Behavioral of kCalculator is
   type state_type is (Idle, Reciving, SumValues, WaitForValue, CalculateK, Sending, ErrorState); -- States for the statemachine
   signal state : state_type;

   signal CheckState    : integer range 0 to 10;--to see what state is currently used for the simulation
   signal CurrentValue  : signed(23 downto 0);
   signal SampleCounter : integer range 0 to 256;--count how many samples have been recived, assuming 256 samples per datablock
   signal TotalSum      : integer range 0 to 1286263056;
begin
   process (clk)
   begin
      if rising_edge(clk) then

         case state is
            when Idle =>
               CheckState <= 0;

               SampleCounter <= 0;
               TotalSum      <= 0;
               ReadyToRecive <= '1';
               NewKOut       <= '0';
               ErrorOut      <= '0';
               CurrentValue  <= (others => '0');

               if NewDataIn = '1' then
                  state <= Reciving;
               end if;

            when Reciving =>
               CheckState <= 1;

               ReadyToRecive <= '0';
               CurrentValue  <= signed(OriginalValue);
               SampleCounter <= SampleCounter + 1;

               state <= SumValues;

            when SumValues =>
               CheckState <= 2;
               --This state summarises the absolute value of all input values
               TotalSum <= TotalSum + to_integer(abs(CurrentValue));

               --if TotalSum is equal or larger than 1261097232 the best k-value is allway 22 (for all inputs of 24 bit signed)
               if TotalSum >= 1261097232 then
                  state <= CalculateK;

                  --if 256 samples have been looked at the full datablock have been sumarised and it is time to find the ideal k-value,
                  -- else another sample is grabbed
               elsif Samplecounter < 256 then
                  state <= WaitForValue;

               else
                  state <= CalculateK;

               end if;

            when WaitForValue =>
               CheckState    <= 3;
               ReadyToRecive <= '1';

               if NewDataIn = '1' then
                  state <= Reciving;
               end if;

            when CalculateK =>
               CheckState <= 4;

               --if statement for differente TotalSum levels to find best k-values
               --these levels have been derive from:
               -- k = log2(log10(2) * x /256) + 1, where x is the TotalSum
               --at every if statement the x value for the given limit is written * 256
               --this is so that it will be easy to calculate new limits if the sample size per block where to change

               if TotalSum < 154112 then--602*256
                  k_value <= "01000";--8

               elsif TotalSum < 307968 then--1203*256
                  k_value <= "01001";--9

               elsif TotalSum < 615936 then--2406*256
                  k_value <= "01010";--10

               elsif TotalSum < 1231616 then--4811*256
                  k_value <= "01011";--11

               elsif TotalSum < 2463232 then--9622*256
                  k_value <= "01100";--12

               elsif TotalSum < 4926208 then--19243*256
                  k_value <= "01101";--13

               elsif TotalSum < 9852416 then--38486*256
                  k_value <= "01110";--14

               elsif TotalSum < 19704576 then--76971*256
                  k_value <= "01111";--15

               elsif TotalSum < 39409152 then--153942*256
                  k_value <= "10000";--16

               elsif TotalSum < 78818048 then--307883*256
                  k_value <= "10001";--17

               elsif TotalSum < 157636096 then--615766*256
                  k_value <= "10010";--18

               elsif TotalSum < 315271936 then--1231531*256
                  k_value <= "10011";--19

               elsif TotalSum < 630543616 then--2463061*256
                  k_value <= "10100";--20

               elsif TotalSum < 1261087232 then--4926122*256
                  k_value <= "10101";--21

               else
                  k_value <= "10110";--22

               end if;

               state <= Sending;

            when Sending =>
               CheckState <= 5;

               NewKOut <= '1';

               state <= Idle;

            when ErrorState =>
               CheckState <= 10;
               ErrorOut <= '1';

         end case;

         if reset = '1' then
            state         <= Idle;
            SampleCounter <= 0;
            TotalSum      <= 0;
            ReadyToRecive <= '0';
            NewKOut       <= '0';
            ErrorOut      <= '0';
            k_value       <= (others => '0');
            k_value       <= "01000";
            CurrentValue  <= (others => '0');

         end if;

      end if;

   end process;

end Behavioral;