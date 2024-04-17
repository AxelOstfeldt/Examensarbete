-- SaveToFile

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity SaveToFile is

   port (
      clk               : in std_logic;
      reset             : in std_logic;
      AssembleDoneIn    : in std_logic;
      AllCodeWordsIn    : in std_logic_vector(8191 downto 0);
      AllCodeWordsLenIn : in std_logic_vector(12 downto 0);

      BitToWrite        : out std_logic;--indicates what bit to write
      WriteBit          : out std_logic;--indicate that there is a bit to write
      DataSavedOut      : out std_logic;

      ErrorOut : out std_logic
   );

end entity;

architecture Behavioral of SaveToFile is
   type state_type is (Idle, Reciving, WriteData, CheckSamples, ErrorState); -- States for the statemachine
   signal state : state_type;

   signal FullLength       : integer range 0 to 8191;
   signal BitsSet          : integer range 0 to 8191;
   signal CurrentCodeWords : std_logic_vector(8191 downto 0);
   signal SamplesWritten   : integer range 0 to 65535;

   signal CheckState : integer range 0 to 10;

begin
   process (clk)
   begin

      if rising_edge(clk) then
         case state is
            when Idle =>
               CheckState       <= 0;
               CurrentCodeWords <= (others => '0');
               BitsSet          <= 0;
               DataSavedOut     <= '1';

               if AssembleDoneIn = '1' then
                  state <= Reciving;

               end if;

            when Reciving =>
               CheckState       <= 1;
               CurrentCodeWords <= AllCodeWordsIn;
               FullLength       <= to_integer(unsigned(AllCodeWordsLenIn));
               DataSavedOut     <= '0';

               state <= WriteData;

            when WriteData =>
               CheckState <= 2;

               --If bitsset is less than fulllength there are still bits from the codeword to be written
               if BitsSet < FullLength then
                  WriteBit <= '1';
                  --write the CurrentCodeWords(8191 - BitsSet) in the text file
                  --preferably on the same line
                  BitToWrite <= CurrentCodeWords(8191 - BitsSet);
                  --Increment bitsset
                  BitsSet <= BitsSet + 1;

               else
                  WriteBit <= '0';
                  --write an empty line in the text file

                  --increment SamplesWritten
                  SamplesWritten <= SamplesWritten + 1;

                  --When all bits are writte go to the next state
                  state <= CheckSamples;

               end if;

            when CheckSamples =>
               CheckState <= 3;

               --if all samples have been written down close the textfile
               --else go to idle and wait for the next codeword

               if SamplesWritten < 256 then
                  state <= Idle;

               else
                  --close the text file
                  state <= ErrorState;

               end if;
            when ErrorState =>
               CheckState <= 10;
               ErrorOut   <= '1';

         end case;

         if reset = '1' then
            DataSavedOut <= '0';
            WriteBit <= '0';

            ErrorOut <= '0';

            CurrentCodeWords <= (others => '0');
            BitsSet          <= 0;
            FullLength       <= 0;

         end if;

      end if;
   end process;
end Behavioral;