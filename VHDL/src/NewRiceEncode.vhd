-- RiceEncoder

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity NewRiceEncoder is

   port (
      reset                   : in std_logic;
      clk                     : in std_logic;
      AllResidualsIn          : in std_logic_vector(1599 downto 0);--value in to be encoded
      kValueIn                : in std_logic_vector(4 downto 0);
      NewKIn                  : in std_logic;--New data available for input
      NewResidualsIn          : in std_logic;
      ReadytoReciveCodeWordIn : in std_logic;

      NewCodeWordReady : out std_logic;--New CodeWord ready to be sent
      ReadyToEncode    : out std_logic;
      CodeWordLen      : out std_logic_vector(9 downto 0);--Bits used in the codeword
      CodeWord         : out std_logic_vector(1023 downto 0);--CodeWord out
      k_valueOut       : out std_logic_vector(4 downto 0);--Behvs den?

      ErrorOut : out std_logic--Send an error signal when error state is reached

   );

end entity;

architecture Behavioral of NewRiceEncoder is
   type state_type is (Idle, Reciving, NewResidual, SetValue, SignBit, FindKLastBits, FindRleCode, RleCoding, SetKLastBits, Sending, ErrorState); -- States for the statemachine
   signal state : state_type;
   --used in all states
   signal LenCounter          : integer range 0 to 1023;--count length of code word
   signal CurrentCodeWord     : std_logic_vector(1023 downto 0);--set bits for current codeword
   signal AllCurrentResiduals : std_logic_vector(1599 downto 0);
   signal CurrentResidual     : std_logic_vector(24 downto 0);
   signal CurrentValue        : signed(24 downto 0);--current value being encoded
   signal k_val_int           : integer range 0 to 32;
   signal k_pow               : integer range 0 to 1073741824;-- max val is 30^2, max val of k^2
   signal abs_bits_set        : integer range 0 to 32;--counts how many of the last bits are set
   signal CheckState          : integer range 0 to 10;--to see what state is currently used for the simulation
   signal ResidualBitCounter  : integer range 0 to 1600;
   signal SampleCounter       : integer range 0 to 64;
   --used in SignBit state
   signal AbsoluteValue : std_logic_vector(24 downto 0);

   --Used in **KLastBits
   signal kLastBits : std_logic_vector(24 downto 0);
   signal kBitsSet  : integer range 0 to 32;

   --Used in **RleCoding
   signal RleBits : std_logic_vector(24 downto 0);
   signal RleLoop : integer range 0 to 1023;



begin
   process (clk)
   begin
      if rising_edge(clk) then

         case state is
            when Idle =>
               --Indicate what the current state is in simulation
               CheckState <= 0;

               -- default values for signals
               k_val_int           <= to_integer(unsigned(kValueIn));
               k_pow               <= 2 ** to_integer(unsigned(kValueIn));
               LenCounter          <= 0;
               CurrentCodeWord     <= (others => '0');
               CurrentValue        <= (others => '0');
               NewCodeWordReady    <= '0';
               AbsoluteValue       <= (others => '0');
               kLastBits           <= (others => '0');
               RleBits             <= (others => '0');
               RleLoop             <= 0;
               abs_bits_set        <= 0;
               kBitsSet            <= 0;
               ErrorOut            <= '0';
               CurrentResidual     <= (others => '0');
               AllCurrentResiduals <= (others => '0');
               ResidualBitCounter  <= 0;
               SampleCounter       <= 0;
               ReadyToEncode       <= '0';

               -- when new data is available go to reciving state
               if (NewKIn = '1') and (NewResidualsIn = '1') then
                  ReadyToEncode <= '1';
                  state <= Reciving;
                  k_valueOut <= kValueIn;
               end if;

            when Reciving =>
               --Indicate what the current state is in simulation
               CheckState    <= 1;
               ReadyToEncode <= '0';

               -- load all residuals
               AllCurrentResiduals <= AllResidualsIn;

               state <= NewResidual;

            when NewResidual =>
               CheckState    <= 2;
               ReadyToEncode <= '0';

               CurrentValue     <= (others => '0');
               NewCodeWordReady <= '0';
               AbsoluteValue    <= (others => '0');
               kLastBits        <= (others => '0');
               RleBits          <= (others => '0');
               RleLoop          <= 0;
               abs_bits_set     <= 0;
               kBitsSet         <= 0;

               --testing
               LenCounter <= 0;
               CurrentCodeWord <= (others => '0');


               --Set the current residual from the datablock with all residuals
               CurrentResidual(24) <= AllCurrentResiduals(1599 - ResidualBitCounter);
               CurrentResidual(23) <= AllCurrentResiduals(1598 - ResidualBitCounter);
               CurrentResidual(22) <= AllCurrentResiduals(1597 - ResidualBitCounter);
               CurrentResidual(21) <= AllCurrentResiduals(1596 - ResidualBitCounter);
               CurrentResidual(20) <= AllCurrentResiduals(1595 - ResidualBitCounter);
               CurrentResidual(19) <= AllCurrentResiduals(1594 - ResidualBitCounter);
               CurrentResidual(18) <= AllCurrentResiduals(1593 - ResidualBitCounter);
               CurrentResidual(17) <= AllCurrentResiduals(1592 - ResidualBitCounter);
               CurrentResidual(16) <= AllCurrentResiduals(1591 - ResidualBitCounter);
               CurrentResidual(15) <= AllCurrentResiduals(1590 - ResidualBitCounter);
               CurrentResidual(14) <= AllCurrentResiduals(1589 - ResidualBitCounter);
               CurrentResidual(13) <= AllCurrentResiduals(1588 - ResidualBitCounter);
               CurrentResidual(12) <= AllCurrentResiduals(1587 - ResidualBitCounter);
               CurrentResidual(11) <= AllCurrentResiduals(1586 - ResidualBitCounter);
               CurrentResidual(10) <= AllCurrentResiduals(1585 - ResidualBitCounter);
               CurrentResidual(9)  <= AllCurrentResiduals(1584 - ResidualBitCounter);
               CurrentResidual(8)  <= AllCurrentResiduals(1583 - ResidualBitCounter);
               CurrentResidual(7)  <= AllCurrentResiduals(1582 - ResidualBitCounter);
               CurrentResidual(6)  <= AllCurrentResiduals(1581 - ResidualBitCounter);
               CurrentResidual(5)  <= AllCurrentResiduals(1580 - ResidualBitCounter);
               CurrentResidual(4)  <= AllCurrentResiduals(1579 - ResidualBitCounter);
               CurrentResidual(3)  <= AllCurrentResiduals(1578 - ResidualBitCounter);
               CurrentResidual(2)  <= AllCurrentResiduals(1577 - ResidualBitCounter);
               CurrentResidual(1)  <= AllCurrentResiduals(1576 - ResidualBitCounter);
               CurrentResidual(0)  <= AllCurrentResiduals(1575 - ResidualBitCounter);
               -- Residual bits can never be larger than 1575, since that gives a negative argument to AllCurrentResiduals
               if ResidualBitCounter < 1551 then
                  --increment ResidualBitCounter so that the next residuals will be grabbed from allresiduals when this state is called next time
                  ResidualBitCounter <= ResidualBitCounter + 25;

               else
                  state <= ErrorState;

               end if;

               --for adjacent each datablock should have 64 residuals, one for every mic in the array
               if SampleCounter < 64 then
                  --increment the sample counter since 1 more residual have been grabbed from all residuals
                  SampleCounter <= SampleCounter + 1;

               else
                  state <= ErrorState;

               end if;
               --when the current residual is grabbed set the value to encode to the current residual
               state <= SetValue;

            when SetValue =>
               CheckState    <= 3;
               ReadyToEncode <= '0';

               CurrentValue <= signed(CurrentResidual);

               state <= SignBit;

            when SignBit =>
               --Indicate what the current state is in simulation
               CheckState    <= 4;
               ReadyToEncode <= '0';

               --Check if CurrentValue is positive or negative, 
               --this decides the sign bit (MSB) for the codeword
               if (to_integer(CurrentValue)) < 0 then
                  CurrentCodeWord(1023 - LenCounter) <= '1';

               else
                  CurrentCodeWord(1023 - LenCounter) <= '0';

               end if;
               --LenCounter cant be larger than 1023, that is the maximum codeword length
               if LenCounter < 1023 then
                  --Increment LenCounter by 1, because 1 bit have been set in the codeword
                  LenCounter <= LenCounter + 1;
               else
                  state <= ErrorState;
               end if;

               --Store the absolute value of CurrentCodeWord
               AbsoluteValue <= std_logic_vector(abs(CurrentValue));
               state         <= FindKLastBits;

            when FindKLastBits =>
               --Indicate what the current state is in simulation
               CheckState    <= 5;
               ReadyToEncode <= '0';

               --set bits so that the k-last bits are saved to later be used in the codeword
               if abs_bits_set < k_val_int then
                  --set the k last bits in the AbsoluteValeue to the kLastBits variable, later to be the k last bits of the codeword
                  kLastBits(abs_bits_set) <= AbsoluteValue(abs_bits_set);
                  abs_bits_set            <= abs_bits_set + 1;

               else

                  --once all bits have been stored go to the next state
                  state <= FindRleCode;
               end if;

            when FindRleCode =>
               --Indicate what the current state is in simulation
               CheckState    <= 6;
               ReadyToEncode <= '0';

               --set the remaining bits in Absolute value to the LSB:s in RleBits to later Run length encode the resulting value
               if abs_bits_set < 25 then
                  RleBits(abs_bits_set - k_val_int) <= AbsoluteValue(abs_bits_set);

                  abs_bits_set <= abs_bits_set + 1;

               else

                  if to_integer(unsigned(RleBits)) > 1023 then
                     --if the int value of RleBits is larger than 1023 the codeword will be to long
                     state <= ErrorState;
                  else

                     --Set the RleBits value as the integer indicating how many ones needs to be Run length encoded
                     RleLoop <= to_integer(unsigned(RleBits));
                     state   <= RleCoding;
                  end if;
               end if;

            when RleCoding =>
               --Indicate what the current state is in simulation
               CheckState    <= 7;
               ReadyToEncode <= '0';

               --If RleLoop is larger than 0, append a 1 to the codeword and decrement RleLoop value
               if RleLoop > 0 then
                  CurrentCodeWord(1023 - LenCounter) <= '1';
                  RleLoop                            <= RleLoop - 1;

                  --LenCounter cant be larger than 1023, that is the maximum codeword length
                  if LenCounter < 1023 then
                     --Increment LenCounter by 1, because 1 bit have been set in the codeword
                     LenCounter <= LenCounter + 1;
                  else
                     state <= ErrorState;
                  end if;

                  --Else the RleCode is set,
                  --set the next bit in the codeword to 0 to indicate that the RLE part of the code word is done
               else
                  CurrentCodeWord(1023 - LenCounter) <= '0';

                  --LenCounter cant be larger than 1023, that is the maximum codeword length
                  if LenCounter < 1023 then
                     --Increment LenCounter by 1, because 1 bit have been set in the codeword
                     LenCounter <= LenCounter + 1;
                  else
                     state <= ErrorState;
                  end if;
                  --go to the next state once RLE coding is done

                  state <= SetKLastBits;

               end if;

            when SetKLastBits =>
               --Indicate what the current state is in simulation
               CheckState    <= 8;
               ReadyToEncode <= '0';

               --set the k-last bits of the code word
               if kBitsSet < k_val_int then
                  --set one bit for each loop until all k last bits are set

                  CurrentCodeWord(1023 - LenCounter) <= kLastBits(k_val_int - 1 - kBitsSet);
                  --LenCounter cant be larger than 1023, that is the maximum codeword length
                  if LenCounter < 1023 then
                     --Increment LenCounter by 1, because 1 bit have been set in the codeword
                     LenCounter <= LenCounter + 1;
                     -- if kBitsSet = k_val_int the codeword is done and the length is precisly enough to hold it,
                     -- but if it is not equal more bits need to be set and the codeword wont be able to fit it
                  elsif kBitsSet /= k_val_int then
                     state <= ErrorState;
                  end if;

                  --increment kBitsSet to set the next bit
                  kBitsSet <= kBitsSet + 1;
               else
                  --The codeword is now finalised,
                  --set the output variables for codeword and codeword length
                  CodeWord    <= CurrentCodeWord;
                  CodeWordLen <= std_logic_vector(to_unsigned(LenCounter, 10));

                  state <= Sending;

               end if;

            when Sending =>
               --Indicate what the current state is in simulation
               CheckState    <= 9;
               ReadyToEncode <= '0';

               --set NewDataOut to 1 to indicate that new data is ready to be sent
               NewCodeWordReady <= '1';

               --wait until CodeWordAssembler is ready to recive the codeword beffore going to the next state
               if ReadytoReciveCodeWordIn = '1' then
                  --If samplecounter = 64 all residuals have been looked at in the datablock, and it is ready to recive a new datablock
                  if SampleCounter = 64 then
                     state <= Idle;

                     --Else the next residual in the current datablock will be grabbed
                  else
                     state <= NewResidual;

                  end if;
               end if;

            when ErrorState =>
               --added State to handle errors
               CHeckState <= 10;
               ErrorOut   <= '1';
         end case;
         if reset = '1' then

            if (to_integer(unsigned(kValueIn)) < 8) or (to_integer(unsigned(kValueIn)) > 22) then
               --k_value have to be atleast 8,
               --to limit max lenght of code words in niche cases
               state <= ErrorState;

            else
               state     <= Idle;
               k_val_int <= to_integer(unsigned(kValueIn));
               k_pow     <= 2 ** to_integer(unsigned(kValueIn));

            end if;

            ErrorOut            <= '0';
            LenCounter          <= 0;
            CurrentCodeWord     <= (others => '0');
            CurrentValue        <= (others => '0');
            NewCodeWordReady    <= '0';
            abs_bits_set        <= 0;
            kBitsSet            <= 0;
            CurrentResidual     <= (others => '0');
            AllCurrentResiduals <= (others => '0');
            ResidualBitCounter  <= 0;
            SampleCounter       <= 0;
            ReadyToEncode       <= '0';
            k_valueOut <= "01000";

         end if;

      end if;

   end process;

end Behavioral;