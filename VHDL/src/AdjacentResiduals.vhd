-- AdjacentResiduals

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all; -- Import the numeric_std package for signed type	

entity AdjacentResiduals is

   port (
      clk   : in std_logic;
      reset : in std_logic;

      DataBlockIn      : in std_logic_vector(1535 downto 0);
      ReadyToEncodeIn  : in std_logic;
      DataBlockReadyIn : in std_logic;
      ReadyToReciveIn  : in std_logic;

      ResidualsCalculatedOut : out std_logic;
      ResidualValueOut       : out std_logic_vector(24 downto 0);
      NewDataOut             : out std_logic;
      AllResidualsOut        : out std_logic_vector(1599 downto 0);
      NewResidualOut         : out std_logic;

      ErrorOut : out std_logic
   );

end entity;

architecture Behavioral of AdjacentResiduals is
   type state_type is (Idle, Reciving, GrabNextValue, CalculateResidual, SetResidualValueOut, SetAllResidualsValue, SendCurrentResidual, SendAllResiduals, ErrorState); -- States for the statemachine
   signal state : state_type;

   signal CurrentDataBlock    : std_logic_vector(1535 downto 0);
   signal mic                 : integer range 0 to 64;
   signal CurrentValue        : std_logic_vector(23 downto 0);
   signal predict_first       : signed(23 downto 0);
   signal prediction          : signed(23 downto 0);
   signal prediction_row      : signed(23 downto 0);
   signal CurrentResidual     : std_logic_vector(24 downto 0);
   signal CheckState          : integer range 0 to 10;
   signal ResidualCounter     : integer range 0 to 1535;
   signal AllResidualsCounter : integer range 0 to 1599;

begin
   process (clk)
   begin
      if rising_edge(clk) then

         case state is
            when Idle =>
               CheckState <= 0;

               --reset all to deafult values
               ResidualsCalculatedOut <= '1';--This is set to '1' to indicate that the code is ready to calculate residuals for a datablock
               ResidualValueOut       <= (others => '0');
               NewDataOut             <= '0';
               AllResidualsOut        <= (others => '0');
               NewResidualOut         <= '0';
               ErrorOut               <= '0';

               mic                 <= 0;
               CurrentValue        <= (others => '0');
               prediction          <= (others => '0');
               prediction_row      <= (others => '0');
               CurrentResidual     <= (others => '0');
               ResidualCounter     <= 0;
               AllResidualsCounter <= 0;

               --Once a new datablock is available go to the next state
               if DataBlockReadyIn = '1' then
                  state <= Reciving;
               end if;

            when Reciving =>
               CheckState <= 1;

               ResidualsCalculatedOut <= '0';
               --Store the datablock
               CurrentDataBlock <= DataBlockIn;

               state <= GrabNextValue;

            when GrabNextValue =>
               CheckState <= 2;
               NewDataOut <= '0';

               --Grab the current value from the datablock
               CurrentValue(23) <= CurrentDataBlock(1535 - ResidualCounter);
               CurrentValue(22) <= CurrentDataBlock(1534 - ResidualCounter);
               CurrentValue(21) <= CurrentDataBlock(1533 - ResidualCounter);
               CurrentValue(20) <= CurrentDataBlock(1532 - ResidualCounter);
               CurrentValue(19) <= CurrentDataBlock(1531 - ResidualCounter);
               CurrentValue(18) <= CurrentDataBlock(1530 - ResidualCounter);
               CurrentValue(17) <= CurrentDataBlock(1529 - ResidualCounter);
               CurrentValue(16) <= CurrentDataBlock(1528 - ResidualCounter);
               CurrentValue(15) <= CurrentDataBlock(1527 - ResidualCounter);
               CurrentValue(14) <= CurrentDataBlock(1526 - ResidualCounter);
               CurrentValue(13) <= CurrentDataBlock(1525 - ResidualCounter);
               CurrentValue(12) <= CurrentDataBlock(1524 - ResidualCounter);
               CurrentValue(11) <= CurrentDataBlock(1523 - ResidualCounter);
               CurrentValue(10) <= CurrentDataBlock(1522 - ResidualCounter);
               CurrentValue(9)  <= CurrentDataBlock(1521 - ResidualCounter);
               CurrentValue(8)  <= CurrentDataBlock(1520 - ResidualCounter);
               CurrentValue(7)  <= CurrentDataBlock(1519 - ResidualCounter);
               CurrentValue(6)  <= CurrentDataBlock(1518 - ResidualCounter);
               CurrentValue(5)  <= CurrentDataBlock(1517 - ResidualCounter);
               CurrentValue(4)  <= CurrentDataBlock(1516 - ResidualCounter);
               CurrentValue(3)  <= CurrentDataBlock(1515 - ResidualCounter);
               CurrentValue(2)  <= CurrentDataBlock(1514 - ResidualCounter);
               CurrentValue(1)  <= CurrentDataBlock(1513 - ResidualCounter);
               CurrentValue(0)  <= CurrentDataBlock(1512 - ResidualCounter);

               -- increment ResidualCounter by 24 so that the next value can be grabbed
               if ResidualCounter > 1488 then
                  state <= ErrorState;

               else
                  ResidualCounter <= ResidualCounter + 24;

               end if;

               state <= CalculateResidual;

            when CalculateResidual =>
               CheckState <= 3;

               --Check if its the first mic
               --if it is use the memory from the previous datablock to predict the value
               if mic = 0 then
                  CurrentResidual <= std_logic_vector(to_signed(to_integer(signed(CurrentValue) - predict_first), 25));
                  --update prediction row to the currentvalue (first mic is also the first in a row)
                  prediction_row <= signed(CurrentValue);
                  --update the first mic value
                  predict_first <= signed(CurrentValue);

               --Check if the current mic is the first mic in a row,
               -- if mic % 8 = 0 it is the first mic in a row
               elsif mic mod 8 = 0 then
                  --Calculate the residual, 
                  --if it is the first mic in the row calculate from the first mic in the previous row
                  CurrentResidual <= std_logic_vector(to_signed(to_integer(signed(CurrentValue) - prediction_row), 25));
                  --update prediction row to the currentvalue
                  prediction_row <= signed(CurrentValue);

               else
                  --Calculate the residual
                  CurrentResidual <= std_logic_vector(to_signed(to_integer(signed(CurrentValue) - prediction), 25));

               end if;

               --Update prediction to the current value
               prediction <= signed(CurrentValue);

               state <= SetResidualValueOut;

            when SetResidualValueOut =>
               CheckState <= 4;

               ResidualValueOut <= CurrentResidual;

               state <= SetAllResidualsValue;

            when SetAllResidualsValue =>
               CheckState <= 5;

               --Set the bits in all Resiudal value
               AllResidualsOut(1599 - AllResidualsCounter) <= CurrentResidual(24);
               AllResidualsOut(1598 - AllResidualsCounter) <= CurrentResidual(23);
               AllResidualsOut(1597 - AllResidualsCounter) <= CurrentResidual(22);
               AllResidualsOut(1596 - AllResidualsCounter) <= CurrentResidual(21);
               AllResidualsOut(1595 - AllResidualsCounter) <= CurrentResidual(20);
               AllResidualsOut(1594 - AllResidualsCounter) <= CurrentResidual(19);
               AllResidualsOut(1593 - AllResidualsCounter) <= CurrentResidual(18);
               AllResidualsOut(1592 - AllResidualsCounter) <= CurrentResidual(17);
               AllResidualsOut(1591 - AllResidualsCounter) <= CurrentResidual(16);
               AllResidualsOut(1590 - AllResidualsCounter) <= CurrentResidual(15);
               AllResidualsOut(1589 - AllResidualsCounter) <= CurrentResidual(14);
               AllResidualsOut(1588 - AllResidualsCounter) <= CurrentResidual(13);
               AllResidualsOut(1587 - AllResidualsCounter) <= CurrentResidual(12);
               AllResidualsOut(1586 - AllResidualsCounter) <= CurrentResidual(11);
               AllResidualsOut(1585 - AllResidualsCounter) <= CurrentResidual(10);
               AllResidualsOut(1584 - AllResidualsCounter) <= CurrentResidual(9);
               AllResidualsOut(1583 - AllResidualsCounter) <= CurrentResidual(8);
               AllResidualsOut(1582 - AllResidualsCounter) <= CurrentResidual(7);
               AllResidualsOut(1581 - AllResidualsCounter) <= CurrentResidual(6);
               AllResidualsOut(1580 - AllResidualsCounter) <= CurrentResidual(5);
               AllResidualsOut(1579 - AllResidualsCounter) <= CurrentResidual(4);
               AllResidualsOut(1578 - AllResidualsCounter) <= CurrentResidual(3);
               AllResidualsOut(1577 - AllResidualsCounter) <= CurrentResidual(2);
               AllResidualsOut(1576 - AllResidualsCounter) <= CurrentResidual(1);
               AllResidualsOut(1575 - AllResidualsCounter) <= CurrentResidual(0);

               --Increment AllResidualsCounter for the next residuals to be set
               if AllResidualsCounter > 1550 then
                  state <= ErrorState;

               else
                  AllResidualsCounter <= AllResidualsCounter + 25;

               end if;

               --increment mic
               if mic < 64 then
                  mic <= mic + 1;

               else
                  state <= ErrorState;

               end if;

               state <= SendCurrentResidual;

            when SendCurrentResidual =>

               CheckState <= 6;
               NewDataOut <= '1';

               if ReadyToReciveIn = '1' then
                  --Check if all mics residuals have been calculated
                  if mic = 64 then
                     --If mic = 64 all mics residuals have been calculated and AllResidualsOut can be sent
                     state <= SendAllResiduals;

                     --if there are more residuals to be calculated in the datablock grab the next value
                  else
                     state <= GrabNextValue;

                  end if;

               end if;
            when SendAllResiduals =>
               CheckState     <= 7;
               NewResidualOut <= '1';

               NewDataOut <= '0';

               if ReadyToEncodeIn = '1' then
                  state <= Idle;

               end if;

            when ErrorState =>
               CheckState <= 10;
               ErrorOut   <= '1';

         end case;

         if reset = '1' then
            state <= Idle;

            ResidualsCalculatedOut <= '0';
            ResidualValueOut       <= (others => '0');
            NewDataOut             <= '0';
            AllResidualsOut        <= (others => '0');
            NewResidualOut         <= '0';
            ErrorOut               <= '0';

            mic                 <= 0;
            CurrentValue        <= (others => '0');
            prediction          <= (others => '0');
            prediction_row      <= (others => '0');
            CurrentResidual     <= (others => '0');
            ResidualCounter     <= 0;
            AllResidualsCounter <= 0;

            predict_first <= (others => '0');

         end if;

      end if;
   end process;

end Behavioral;