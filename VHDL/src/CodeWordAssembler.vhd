-- RiceEncoder

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity CodeWordAssembler is

   port (
      reset              : in std_logic;
      clk                : in std_logic;
      CodeWordIn         : in std_logic_vector(1023 downto 0);--CodeWord
      CodeWordLenIn      : in std_logic_vector(9 downto 0);
      k_valueIn          : in std_logic_vector(4 downto 0);--Saved as metadata
      NewCodeWordReadyIn : in std_logic;--New codeword available for assemble
      DataSavedIn        : std_logic;

      AllCodeWordsOut          : out std_logic_vector(8191 downto 0);--All codewords together, length is 2^13 - 1
      AssembleDoneOut          : out std_logic;--New CodeWord ready to be sent
      ReadyToReciveCodeWordOut : out std_logic;--Indicates that it is ready to recive the next codeword to assemble
      AllCodeWordsLenOut       : out std_logic_vector(12 downto 0);


      ErrorOut                 : out std_logic--Send an error signal when error state is reached

   );

end entity;

architecture Behavioral of CodeWordAssembler is
   type state_type is (Idle, WaitForCodeWord, Reciving, LengthCheck, Assemble, SetMetaData, Sending, ErrorState); -- States for the statemachine
   signal state : state_type;
   --used in all states
   signal TotalLenCounter    : integer range 0 to 8191;--count the length off all the assembled codewords
   signal CurrentCodeWordLen : integer range 0 to 1023;--length of the current codeword
   signal AssembleLenCounter : integer range 0 to 1024;--count how many bits of the current codeword have been assembled
   signal SampleCounter      : integer range 0 to 256;--counts how many codewords have been recived
   signal SampleCounter_meta : std_logic_vector(7 downto 0);--SampleCounter as binary metadata
   signal CurrentCodeWord    : std_logic_vector(1023 downto 0);--set bits for current codeword
   signal k_meta             : std_logic_vector(4 downto 0);
   signal CheckState         : integer range 0 to 10;--to see what state is currently used for the simulation
begin
   process (clk)
   begin
      if rising_edge(clk) then

         case state is
            when Idle =>
               CheckState <= 0;
               --Reset all values
               AllCodeWordsOut    <= (others => '0');
               AllCodeWordsLenOut <= (others => '0');
               ErrorOut           <= '0';
               AssembleDoneOut    <= '0';
               TotalLenCounter    <= 0;
               CurrentCodeWordLen <= 0;
               AssembleLenCounter <= 0;
               CurrentCodeWord    <= (others => '0');
               k_meta             <= (others => '0');
               SampleCounter      <= 0;
               SampleCounter_meta <= (others => '0');
               if NewCodeWordReadyIn = '1' then
                  state                    <= Reciving;


               end if;

               ReadyToReciveCodeWordOut <= '1';

            when WaitForCodeWord =>
               CheckState <= 1;

               if NewCodeWordReadyIn = '1' then
                  state                    <= Reciving;

               end if;
      
               ReadyToReciveCodeWordOut <= '1';


            when Reciving =>
               CheckState               <= 2;
               ReadyToReciveCodeWordOut <= '0';
               --if it is the first codeword to be assembled the k_value is saved to later be used as meta data
               if TotalLenCounter = 0 then
                  k_meta <= k_valueIn;
               end if;

               --Grab the current recived CodeWord
               CurrentCodeWord <= CodeWordIn;
               --Reset assembled bits counter
               AssembleLenCounter <= 0;
               --Grab the length of the current codeword
               CurrentCodeWordLen <= to_integer(unsigned(CodeWordLenIn));
               state              <= LengthCheck;

               --length check state to see that currentcodeword fits, totallen + currentlen < 6143

            when LengthCheck =>
               CheckState <= 3;
               --If adding the new codeword to the assembled codewords creates a to long vector the codeword can not be added
               --The metadata is instead added on and the assembled codeword can be sent
               if (CurrentCodeWordLen + TotalLenCounter) > 8191 then
                  --SampleCounter is decremented by 1, so that it can be saved as a 8 bit value (since 0 samples will never be sent anyway)
                  if SampleCounter = 0 then
                     state <= ErrorState;

                  else
                     SampleCounter_meta <= std_logic_vector(to_unsigned(SampleCounter - 1, 8));
                     state              <= SetMetaData;

                  end if;

               else
                  --The codeword can be added and the Samplecounter is incremented by 1
                  SampleCounter <= SampleCounter + 1;
                  state         <= Assemble;

               end if;

            when Assemble =>
               CheckState <= 4;
               --if AssembleLenCounter is larger than CurrentCodeWordLen all bits in the codeword have been assembled
               if AssembleLenCounter < CurrentCodeWordLen then
                  --Assemble the codewords with eachother in "AllCodeWords"
                  --first 13 bits are for metadata
                  AllCodeWordsOut(8178 - TotalLenCounter) <= CurrentCodeWord(1023 - AssembleLenCounter);
                  --Increment the assembleLenCOunter by 1
                  AssembleLenCounter <= AssembleLenCounter + 1;

                  --Increment the total length of all codewords by 1
                  TotalLenCounter <= TotalLenCounter + 1;

                  --once all the bits in the current codeword have been assembled check if all 256 samples have been recived
                  --if the SampleCounter is less than 256 recive another sample
               elsif SampleCounter < 64 then
                  state <= WaitForCodeWord;

                  --if all the samples have been assembled set the metadata
               else
                  --SampleCounter is decremented by 1, so that it can be saved as a 8 bit value (since 0 samples will never be sent anyway)
                  if SampleCounter = 0 then
                     state <= ErrorState;
                  else
                     SampleCounter_meta <= std_logic_vector(to_unsigned(SampleCounter - 1, 8));
                     TotalLenCounter    <= TotalLenCounter + 13;--13 bits of meta data
                     state              <= SetMetaData;
                  end if;
               end if;

            when SetMetaData =>
               CheckState <= 5;

               --Set total len for codeword out
               AllCodeWordsLenOut <= std_logic_vector(to_unsigned(TotalLenCounter, 13));

               --Set the k-value meta data
               AllCodeWordsOut(8191) <= k_meta(4);
               AllCodeWordsOut(8190) <= k_meta(3);
               AllCodeWordsOut(8189) <= k_meta(2);
               AllCodeWordsOut(8188) <= k_meta(1);
               AllCodeWordsOut(8187) <= k_meta(0);

               --Set the SampleCounter metadata
               AllCodeWordsOut(8186) <= SampleCounter_meta(7);
               AllCodeWordsOut(8185) <= SampleCounter_meta(6);
               AllCodeWordsOut(8184) <= SampleCounter_meta(5);
               AllCodeWordsOut(8183) <= SampleCounter_meta(4);
               AllCodeWordsOut(8182) <= SampleCounter_meta(3);
               AllCodeWordsOut(8181) <= SampleCounter_meta(2);
               AllCodeWordsOut(8180) <= SampleCounter_meta(1);
               AllCodeWordsOut(8179) <= SampleCounter_meta(0);
               state                 <= Sending;

            when Sending =>
               CheckState      <= 6;
               AssembleDoneOut <= '1';
               if DataSavedIn = '1' then
                  state <= Idle;
               end if;

            when ErrorState =>
               CheckState <= 10;
               ErrorOut   <= '1';
         end case;

         if reset = '1' then
            state                    <= Idle;
            AllCodeWordsOut          <= (others => '0');
            AllCodeWordsLenOut       <= (others => '0');
            ErrorOut                 <= '0';
            AssembleDoneOut          <= '0';
            TotalLenCounter          <= 0;
            CurrentCodeWordLen       <= 0;
            AssembleLenCounter       <= 0;
            CurrentCodeWord          <= (others => '0');
            SampleCounter            <= 0;
            SampleCounter_meta       <= (others => '0');
            k_meta                   <= (others => '0');
            ReadyToReciveCodeWordOut <= '0';

         end if;

      end if;

   end process;

end Behavioral;