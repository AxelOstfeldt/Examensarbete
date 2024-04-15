-- kCalculator

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity kCalculator is

   port (
      reset           : in std_logic;
      clk             : in std_logic;
      ResidualValueIn : in std_logic_vector(24 downto 0);--value in to be encoded
      NewDataIn       : in std_logic;--New data available for input
      ReadyToEncode   : in std_logic;

      ReadyToReciveOut : out std_logic;
      NewKOut          : out std_logic;--New k-value to be sent
      kValueOut        : out std_logic_vector(4 downto 0);--k-value between 0 and 31
      ErrorOut         : out std_logic--Send an error signal when error state is reached

   );

end entity;

architecture Behavioral of kCalculator is
   type state_type is (Idle, Reciving, SumValues, WaitForValue, CalculateK, Sending, ErrorState); -- States for the statemachine
   signal state : state_type;

   signal CheckState    : integer range 0 to 10;--to see what state is currently used for the simulation
   signal CurrentValue  : signed(24 downto 0);
   signal SampleCounter : integer range 0 to 256;--count how many samples have been recived, assuming maximum 256 samples per datablock
   signal TotalSum      : integer range 0 to 1300000000;
begin
   process (clk)
   begin
      if rising_edge(clk) then

         case state is
            when Idle =>
               CheckState <= 0;

               SampleCounter    <= 0;
               TotalSum         <= 0;
               ReadyToReciveOut <= '1';
               NewKOut          <= '0';
               ErrorOut         <= '0';
               CurrentValue     <= (others => '0');

               if NewDataIn = '1' then
                  state <= Reciving;
               end if;

            when Reciving =>
               CheckState <= 1;

               ReadyToReciveOut <= '0';
               CurrentValue     <= signed(ResidualValueIn);
               SampleCounter    <= SampleCounter + 1;

               state <= SumValues;

            when SumValues =>
               CheckState <= 2;
               --This state summarises the absolute value of all input values
               TotalSum <= TotalSum + to_integer(abs(CurrentValue));

               --if TotalSum is equal or larger than 1261097232 the best k-value is allway 22 (for all inputs of 24 bit signed)
               --This limit is set after "4 926 122*256", since if that value is reached for totalsum k will allways be 22.
               --This assumes that 256 samples will be used, however when looking at just one microphone array only 64 samples per datablock is used
               --The limit could therefore be lowered. 
               if TotalSum >= 1261087232 then
                  state <= CalculateK;

                  --if 64 samples (assuming 64 samples per datablock, if more samples per data block is used this number needs to adapt after it)
                  --have been looked at the full datablock have been sumarised and it is time to find the ideal k-value,
                  -- else another sample is grabbed
               elsif Samplecounter < 64 then
                  state <= WaitForValue;

               else
                  state <= CalculateK;

               end if;

            when WaitForValue =>
               CheckState       <= 3;
               ReadyToReciveOut <= '1';

               if NewDataIn = '1' then
                  state <= Reciving;
               end if;

            when CalculateK =>
               CheckState <= 4;

               --if statement for differente TotalSum levels to find best k-values
               --these levels have been derive from:
               -- k = log2(log10(2) * x /s ) + 1, where "x" is the TotalSum and "s" is the total amount of samples
               -- to avoid devision the limits for the total sum have been pre calculated
               -- the limits assume 64 datasamples per datablock, this is one microphone array.
               -- but the limits for all microphones, 256 samples per datablock have also been calculated and can be found in the comment
               -- along with how the calculations was made so that the limit can easily be adjusted in the future by multiplying with a new amount of samples

               if TotalSum < 38528 then--602*64 = 38 528, 602*256 = 154112
                  kValueOut <= "01000";--8

               elsif TotalSum <  76992 then--1203 * 64 = 76 992, 1203*256 = 307968
                  kValueOut <= "01001";--9

               elsif TotalSum < 153984 then--2406 * 64 = 153 984, 2406*256 = 615936
                  kValueOut <= "01010";--10

               elsif TotalSum < 307904 then--4811 * 64 = 307 904, 4811*256 = 1231616
                  kValueOut <= "01011";--11

               elsif TotalSum < 615808 then--9622 * 64 = 615 808, 9622*256 = 2463232
                  kValueOut <= "01100";--12

               elsif TotalSum < 1231552 then--19234 * 64 = 1 231 552, 19243*256 = 4926208
                  kValueOut <= "01101";--13

               elsif TotalSum < 2463104 then--38486 * 64 = 2 463 104,38486*256 = 9852416
                  kValueOut <= "01110";--14

               elsif TotalSum < 4926144 then--76971 * 64 = 4 926 144, 76971*256 = 19704576
                  kValueOut <= "01111";--15

               elsif TotalSum < 9852288 then--153942 * 64 = 9 852 288, 153942*256 = 39409152
                  kValueOut <= "10000";--16

               elsif TotalSum < 19704512 then--307 883 * 64 = 19 704 512, 307883*256 = 78818048
                  kValueOut <= "10001";--17

               elsif TotalSum < 39409024 then--615 766 * 64 = 39 409 024, 615766*256 = 157636096
                  kValueOut <= "10010";--18

               elsif TotalSum < 78817984 then--1 231 531 * 64 = 78 817 984, 1231531*256 = 315271936
                  kValueOut <= "10011";--19

               elsif TotalSum < 157635904 then--2 463 061 * 64 = 157 635 904, 2463061*256 = 630543616
                  kValueOut <= "10100";--20

               elsif TotalSum < 315271808 then--4 926 122 * 64 = 315 271 808, 4926122*256 = 1261087232
                  kValueOut <= "10101";--21

               else
                  kValueOut <= "10110";--22

               end if;

               state <= Sending;

            when Sending =>
               CheckState <= 5;

               --New k value calculated, ready to be sent out
               NewKOut <= '1';

               --Once ready to encode is =1 RiceEncoder block is ready to recive the new k-value
               --When it have been sent return to idle state to wait for the next residuals to calculate new k-value
               if ReadyToEncode = '1' then
                  state <= Idle;
               end if;

            when ErrorState =>
               CheckState <= 10;
               ErrorOut   <= '1';

         end case;

         if reset = '1' then
            state            <= Idle;
            SampleCounter    <= 0;
            TotalSum         <= 0;
            ReadyToReciveOut <= '0';
            NewKOut          <= '0';
            ErrorOut         <= '0';
            kValueOut        <= (others => '0');
            kValueOut        <= "01000";
            CurrentValue     <= (others => '0');

         end if;

      end if;

   end process;

end Behavioral;