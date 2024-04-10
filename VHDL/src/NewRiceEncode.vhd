-- RiceEncoder

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity NewRiceEncoder is

   port (
      reset         : in std_logic;
      clk           : in std_logic;
      OriginalValue : in std_logic_vector(23 downto 0);--value in to be encoded
      k_value       : in std_logic_vector(4 downto 0);
      NewDataIn     : in std_logic;--New data available for input

      NewDataOut     : out std_logic;--New CodeWord ready to be sent
      CodeWordLength : out std_logic_vector(4 downto 0);--Bits used in the codeword
      CodeWord       : out std_logic_vector(23 downto 0)--CodeWord out

   );

end entity;

architecture Behavioral of NewRiceEncoder is
   type state_type is (Idle, Reciving, SignBit, FindKLastBits, FindRleCode, RleCoding, SetKLastBits, Sending); -- States for the statemachine
   signal state : state_type;
   --used in all states
   signal LenCounter      : integer range 0 to 32;--count length of code word
   signal CurrentCodeWord : std_logic_vector(23 downto 0);--set bits for current codeword
   signal CurrentValue    : signed(23 downto 0);--current value being encoded
   signal k_val_int       : integer range 0 to 32;
   signal k_pow           : integer range 1 to 1073741824;-- max val is 30^2, max val of k^2
   signal abs_bits_set    : integer range 0 to 32;--counts how many of the last bits are set
   signal CheckState      : integer range 0 to 10;--to see what state is currently used for the simulation

   --used in SignBit state
   signal AbsoluteValue : std_logic_vector(23 downto 0);

   --Used in **KLastBits
   signal kLastBits : std_logic_vector(23 downto 0);
   signal kBitsSet  : integer range 0 to 32;

   --Used in **RleCoding
   signal RleBits : std_logic_vector(23 downto 0);
   signal RleLoop : integer range 0 to 23;

begin
   process (clk)
   begin
      if rising_edge(clk) then

         case state is
            when Idle =>
               --Indicate what the current state is in simulation
               CheckState <= 0;

               -- default values for signals
               k_val_int       <= to_integer(unsigned(k_value));
               k_pow           <= 2 ** to_integer(unsigned(k_value));
               LenCounter      <= 0;
               CurrentCodeWord <= (others => '0');
               CurrentValue    <= (others => '0');
               NewDataOut      <= '0';
               AbsoluteValue   <= (others => '0');
               kLastBits       <= (others => '0');
               RleBits         <= (others => '0');
               RleLoop         <= 0;
               abs_bits_set    <= 0;
               kBitsSet        <= 0;

               -- when new data is available go to reciving state
               if NewDataIn = '1' then
                  state <= Reciving;
               end if;

            when Reciving =>
               --Indicate what the current state is in simulation
               CheckState <= 1;

               -- load the new Codeword
               CurrentValue <= signed(OriginalValue);

               --when data is loaded go to SignBit state
               state <= SignBit;

            when SignBit =>
               --Indicate what the current state is in simulation
               CheckState <= 2;

               --Check if CurrentValue is positive or negative, 
               --this decides the sign bit (MSB) for the codeword
               if (to_integer(CurrentValue)) < 0 then
                  CurrentCodeWord(23 - LenCounter) <= '1';

               else
                  CurrentCodeWord(23 - LenCounter) <= '0';

               end if;

               --Increment LenCounter by 1, because 1 bit have been set in the codeword
               LenCounter <= LenCounter + 1;

               --Store the absolute value of CurrentCodeWord
               AbsoluteValue <= std_logic_vector(abs(CurrentValue));
               state         <= FindKLastBits;

            when FindKLastBits =>
               --Indicate what the current state is in simulation
               CheckState <= 3;

               --set bits so that the k-last bits are saved to later be used in the codeword
               if abs_bits_set < k_val_int then
                  --set the k last bits in the AbsoluteValeue to the kLastBits variable, later to be the k last bits of the codeword
                  kLastBits(abs_bits_set) <= AbsoluteValue(abs_bits_set);
                  abs_bits_set <= abs_bits_set + 1;

               else

                  --once all bits have been stored go to the next state
                  state     <= FindRleCode;
               end if;

            when FindRleCode =>
               --Indicate what the current state is in simulation
               CheckState <= 4;

               --set the remaining bits in Absolute value to the LSB:s in RleBits to later Run length encode the resulting value
               if abs_bits_set < 24 then
                  RleBits(abs_bits_set - k_val_int) <= AbsoluteValue(abs_bits_set);

                  abs_bits_set <= abs_bits_set + 1;

               else
                  --Set the RleBits value as the integer indicating how many ones needs to be Run length encoded
                  RleLoop <= to_integer(unsigned(RleBits));
                  state   <= RleCoding;

               end if;

            when RleCoding =>
               --Indicate what the current state is in simulation
               CheckState <= 5;

               --If RleLoop is larger than 0, append a 1 to the codeword and decrement RleLoop value
               if RleLoop > 0 then
                  CurrentCodeWord(23 - LenCounter) <= '1';
                  RleLoop                          <= RleLoop - 1;

                  --increment LenCounter since another bit have been set in the codeword
                  LenCounter <= LenCounter + 1;

                  --Else the RleCode is set,
                  --set the next bit in the codeword to 0 to indicate that the RLE part of the code word is done
               else
                  CurrentCodeWord(23 - LenCounter) <= '0';
                  LenCounter                       <= LenCounter + 1;

                  --go to the next state once RLE coding is done

                  state <= SetKLastBits;

               end if;


            when SetKLastBits =>
               --Indicate what the current state is in simulation
               CheckState <= 6;

               --set the k-last bits of the code word
               if kBitsSet < k_val_int then
                  --set one bit for each loop until all k last bits are set
                  CurrentCodeWord(23 - LenCounter) <= kLastBits(k_val_int - 1 - kBitsSet);
                  --increment kBitsSet to set the next bit
                  kBitsSet <= kBitsSet + 1;

                  --increment LenCounter since another bit have been set in the codeword
                  LenCounter <= LenCounter + 1;

               else
                  --The codeword is now finalised,
                  --set the output variables for codeword and codeword length
                  CodeWord       <= CurrentCodeWord;
                  CodeWordLength <= std_logic_vector(to_unsigned(LenCounter, 5));

                  state <= Sending;

               end if;

            when Sending =>
               --Indicate what the current state is in simulation
               CheckState <= 7;

               --set NewDataOut to 1 to indicate that new data is ready to be sent
               NewDataOut <= '1';

               state <= Idle;

         end case;
         if reset = '1' then
            k_val_int       <= to_integer(unsigned(k_value));
            LenCounter      <= 0;
            CurrentCodeWord <= (others => '0');
            CurrentValue    <= (others => '0');
            k_pow           <= 2 ** to_integer(unsigned(k_value));
            NewDataOut      <= '0';
            state           <= Idle;
            abs_bits_set    <= 0;
            kBitsSet        <= 0;
         end if;

      end if;

   end process;

end Behavioral;
