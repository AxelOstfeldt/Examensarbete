library IEEE;
use IEEE.STD_LOGIC_1164.all;
use ieee.numeric_std.all;
use std.textio.all;

library vunit_lib;
context vunit_lib.vunit_context;

use work.MATRIX_TYPE.all;

entity tb_adjacent_combined is
   generic (
      runner_cfg : string
   );

end tb_adjacent_combined;

architecture adjacent_combined_arch of tb_adjacent_combined is

   --General signals used in all entitys
   constant C_SCK_CYKLE : time      := 8 ns; -- 125 MHz
   signal clk_tb        : std_logic := '0';
   signal reset_tb      : std_logic := '1';

   --Used for LoadData(Only testbench no entity)
   signal CurrentValue_tb  : std_logic_vector(23 downto 0);
   signal SampleCounter_tb : integer range 0 to 65535;
   signal MicCounter_tb    : integer range 0 to 65535;
   signal InputCounter_tb  : integer range 0 to 1535;

   signal EndOfFileReached_tb : std_logic;

   signal DatablockOut_tb          : std_logic_vector(1535 downto 0);
   signal DataBlockReadyOut_tb     : std_logic;
   signal ResidualsCalculatedIn_tb : std_logic;

   --Used for SaveToFile(Only testbench no entity)
   signal NewRow_tb      : std_logic;
   signal BottomLimit_tb : integer range 0 to 8191;
   signal RowCounter_tb  : integer range 0 to 65535;
   signal AllDone        : std_logic;
   signal LengthError    : std_logic;

   --Used in AdjacentResiduals
   signal DataBlockIn_tb      : std_logic_vector(1535 downto 0);
   signal ReadyToEncodeIn_tb  : std_logic;
   signal DataBlockReadyIn_tb : std_logic;
   signal ReadyToReciveIn_tb  : std_logic;

   signal ResidualsCalculatedOut_tb : std_logic;
   signal ResidualValueOut_tb       : std_logic_vector(24 downto 0);
   signal NewDataOut_tb             : std_logic;
   signal AllResidualsOut_tb        : std_logic_vector(1599 downto 0);
   signal NewResidualOut_tb         : std_logic;

   signal ErrorOut_Adjacent_tb : std_logic;

   --Used in kCalculator
   signal ResidualValueIn_tb            : std_logic_vector(24 downto 0);--value in to be encoded
   signal NewDataIn_tb                  : std_logic;--New data available for input
   signal ReadyToEncodeInkCalculator_tb : std_logic;

   signal ReadyToReciveOut_tb : std_logic;
   signal NewKOut_tb          : std_logic;--New k-value to be sent
   signal ErrorOut_tb         : std_logic;--Send an error signal when error state is reached
   signal kValueOut_tb        : std_logic_vector(4 downto 0);

   signal ErrorOut_kCalculator_tb : std_logic;

   --Used in RiceEncode
   signal AllResidualsIn_tb          : std_logic_vector(1599 downto 0);
   signal kValueIn_tb                : std_logic_vector(4 downto 0);
   signal NewKIn_tb                  : std_logic;--New data available for input
   signal NewResidualsIn_tb          : std_logic;
   signal ReadytoReciveCodeWordIn_tb : std_logic;

   signal NewCodeWordReady_tb : std_logic;--New CodeWord ready to be sent
   signal CodeWordLen_tb      : std_logic_vector(9 downto 0);--Bits used in the codeword
   signal CodeWord_tb         : std_logic_vector(1023 downto 0);--CodeWord out
   signal ReadyToEncode_tb    : std_logic;
   signal k_valueOut_tb       : std_logic_vector(4 downto 0);

   signal ErrorOut_RiceEncode_tb : std_logic;

   --Used in CodeWordAssembler
   signal CodeWordIn_tb         : std_logic_vector(1023 downto 0);--CodeWord
   signal CodeWordLenIn_tb      : std_logic_vector(9 downto 0);
   signal k_valueIn_tb          : std_logic_vector(4 downto 0);--Saved as metadata
   signal NewCodeWordReadyIn_tb : std_logic;--New codeword available for assemble
   signal DataSavedIn_tb        : std_logic;

   signal AllCodeWordsOut_tb          : std_logic_vector(8191 downto 0);--All codewords together, length is 2^13 - 1
   signal AssembleDoneOut_tb          : std_logic;--New CodeWord ready to be sent
   signal ReadyToReciveCodeWordOut_tb : std_logic;
   signal AllCodeWordsLenOut_tb       : std_logic_vector(12 downto 0);

   signal ErrorOut_CodeWordAssmbler_tb : std_logic;

   --Signals used in testbench
   signal InputState_tb  : std_logic_vector(1 downto 0);
   signal OutputState_tb : std_logic_vector(1 downto 0);
   signal CreateInput_tb : std_logic_vector(23 downto 0);

begin
   clk_tb <= not(clk_tb) after C_SCK_CYKLE/2;

   reset_tb <= '1', '0' after 35 ns;

   --AdjacentResiduals entity
   AdjacentResidualsTest : entity work.AdjacentResiduals
      port map(
         clk   => clk_tb,
         reset => reset_tb,

         DataBlockIn      => DataBlockIn_tb,
         ReadyToEncodeIn  => ReadyToEncodeIn_tb,
         DataBlockReadyIn => DataBlockReadyIn_tb,
         ReadyToReciveIn  => ReadyToReciveIn_tb,

         ResidualsCalculatedOut => ResidualsCalculatedOut_tb,
         ResidualValueOut       => ResidualValueOut_tb,
         NewDataOut             => NewDataOut_tb,
         AllResidualsOut        => AllResidualsOut_tb,
         NewResidualOut         => NewResidualOut_tb,

         ErrorOut => ErrorOut_Adjacent_tb
      );

   --kCalculator entity
   kCalculatorTest : entity work.kCalculator
      port map(
         reset                      => reset_tb,
         clk                        => clk_tb,
         ResidualValueIn            => ResidualValueIn_tb,
         NewDataIn                  => NewDataIn_tb,
         ReadyToEncodeInkCalculator => ReadyToEncodeInkCalculator_tb,

         ReadyToReciveOut => ReadyToReciveOut_tb,
         NewKOut          => NewKOut_tb,
         kValueOut        => kValueOut_tb,

         ErrorOut => ErrorOut_kCalculator_tb
      );

   --RiceEncode entity
   RiceEncoderTest : entity work.NewRiceEncoder
      port map(
         reset                   => reset_tb,
         clk                     => clk_tb,
         AllResidualsIn          => AllResidualsIn_tb,
         kValueIn                => kValueIn_tb,
         NewResidualsIn          => NewResidualsIn_tb,
         NewKIn                  => NewKIn_tb,
         ReadytoReciveCodeWordIn => ReadytoReciveCodeWordIn_tb,

         NewCodeWordReady => NewCodeWordReady_tb,
         CodeWordLen      => CodeWordLen_tb,
         CodeWord         => CodeWord_tb,
         ReadyToEncode    => ReadyToEncode_tb,
         k_valueOut       => k_valueOut_tb,

         ErrorOut => ErrorOut_RiceEncode_tb
      );

   --CodeWordAssembler entity
   TestCodeWordAssembler : entity work.CodeWordAssembler
      port map(
         reset => reset_tb,
         clk   => clk_tb,

         CodeWordIn         => CodeWordIn_tb,
         CodeWordLenIn      => CodeWordLenIn_tb,
         k_valueIn          => k_valueIn_tb,
         NewCodeWordReadyIn => NewCodeWordReadyIn_tb,
         DataSavedIn        => DataSavedIn_tb,

         AllCodeWordsOut          => AllCodeWordsOut_tb,
         AssembleDoneOut          => AssembleDoneOut_tb,
         ReadyToReciveCodeWordOut => ReadyToReciveCodeWordOut_tb,
         AllCodeWordsLenOut       => AllCodeWordsLenOut_tb,

         ErrorOut => ErrorOut_CodeWordAssmbler_tb
      );
   ws_process_12345 : process (clk_tb)

      --For reading data
      variable text_line : line;
      variable row_value : std_logic_vector(23 downto 0);
      --Make sure this directiory is correct!
      --file my_file : text open read_mode is "/home/toad/Projects/FPGA-sampling2/pl/test/first_sample_binary.txt";--First sample for mic 64-127
      --file my_file : text open read_mode is "/home/toad/Projects/FPGA-sampling2/pl/test/data_block_binary.txt";--First datablock, all 256 samples for mic 64-12
      file my_file : text open read_mode is "C:\\Users\\axelo\\OneDrive\\Skrivbord\\Exjobb\\GIT\\SoundData\\VHDL\\data_block_binary.txt";--First datablock, all 256 samples for mic 64-12
      
      --For saving data
      --Importent to check path /My/Path/MyFileName.txt
      --file file_handler     : text open write_mode is "/home/toad/Projects/FPGA-sampling2/pl/test/EncodedData.txt";
      file file_handler     : text open write_mode is "C:\\Users\\axelo\\OneDrive\\Skrivbord\\Exjobb\\GIT\\SoundData\\VHDL\\EncodedData.txt";
      variable row          : line;
      variable v_data_write : std_logic_vector(8191 downto 0);
   begin

      if falling_edge(clk_tb) then

         if InputState_tb = "01" then
            --This is the starting state when grabbing a datablock
            DatablockOut_tb      <= (others => '0');
            DataBlockReadyOut_tb <= '0';

            CurrentValue_tb <= (others => '0');
            MicCounter_tb   <= 0;
            InputCounter_tb <= 0;

            InputState_tb <= "10";

         elsif InputState_tb = "10" then
            --check that it is not end of file
            if not endfile(my_file) then
               --point to the next line
               readline(my_file, text_line);
               --read the current lint
               read(text_line, row_value);

               
               --assign CurrentValue_tb with the read value from text file
               CurrentValue_tb <= row_value;-- only to see current value

               --set input values for testbench
               DataBlockOut_tb(1535 - InputCounter_tb) <= row_value(23);
               DataBlockOut_tb(1534 - InputCounter_tb) <= row_value(22);
               DataBlockOut_tb(1533 - InputCounter_tb) <= row_value(21);
               DataBlockOut_tb(1532 - InputCounter_tb) <= row_value(20);
               DataBlockOut_tb(1531 - InputCounter_tb) <= row_value(19);
               DataBlockOut_tb(1530 - InputCounter_tb) <= row_value(18);
               DataBlockOut_tb(1529 - InputCounter_tb) <= row_value(17);
               DataBlockOut_tb(1528 - InputCounter_tb) <= row_value(16);
               DataBlockOut_tb(1527 - InputCounter_tb) <= row_value(15);
               DataBlockOut_tb(1526 - InputCounter_tb) <= row_value(14);
               DataBlockOut_tb(1525 - InputCounter_tb) <= row_value(13);
               DataBlockOut_tb(1524 - InputCounter_tb) <= row_value(12);
               DataBlockOut_tb(1523 - InputCounter_tb) <= row_value(11);
               DataBlockOut_tb(1522 - InputCounter_tb) <= row_value(10);
               DataBlockOut_tb(1521 - InputCounter_tb) <= row_value(9);
               DataBlockOut_tb(1520 - InputCounter_tb) <= row_value(8);
               DataBlockOut_tb(1519 - InputCounter_tb) <= row_value(7);
               DataBlockOut_tb(1518 - InputCounter_tb) <= row_value(6);
               DataBlockOut_tb(1517 - InputCounter_tb) <= row_value(5);
               DataBlockOut_tb(1516 - InputCounter_tb) <= row_value(4);
               DataBlockOut_tb(1515 - InputCounter_tb) <= row_value(3);
               DataBlockOut_tb(1514 - InputCounter_tb) <= row_value(2);
               DataBlockOut_tb(1513 - InputCounter_tb) <= row_value(1);
               DataBlockOut_tb(1512 - InputCounter_tb) <= row_value(0);

               if InputCounter_tb < 1489 then

                  --increment InputCounter_tb to set the nxt 24 values for the next mic
                  InputCounter_tb <= InputCounter_tb + 24;
               end if;

               --increment mic
               if MicCounter_tb < 63 then
                  --if all 63 mics have not been set grab the next mic value
                  MicCounter_tb <= MicCounter_tb + 1;
                  InputState_tb <= "10";

               else
                  InputState_tb <= "00";

                  --increment the sample counter
                  SampleCounter_tb <= SampleCounter_tb + 1;

                  --Set DataBlockReadyOut_tb to high to indicate that the datablock is done
                  DataBlockReadyOut_tb <= '1';

               end if;

            else
               EndOfFileReached_tb <= '1';
               InputState_tb <= "11";

            end if;

         elsif InputState_tb = "00" then

            if ResidualsCalculatedIn_tb = '1' then
               --once AdjacentResidual have recived the datablock (ResidualsCalculatedIn_tb is high)
               --start createing the next datablock
               InputState_tb <= "01";

            end if;

         end if;



         if OutputState_tb <= "01" then

            DataSavedIn_tb <= '1';

            --Once the full codeword is assembled and ready to be sent the next state is entered
            if AssembleDoneOut_tb = '1' then
               --store All CodeWords and the length of them 
               v_data_write := AllCodeWordsOut_tb;
               if to_integer(unsigned(AllCodeWordsLenOut_tb)) > 0 then
                  BottomLimit_tb <= to_integer(unsigned(AllCodeWordsLenOut_tb) - 1);

               else

                  BottomLimit_tb <= to_integer(unsigned(AllCodeWordsLenOut_tb));
                  LengthError <= '1';
               end if;

               OutputState_tb <= "10";

            end if;
         elsif OutputState_tb <= "10" then

            --This indicated that the codeword can be saved and the next assemble can start
            DataSavedIn_tb <= '0';
            if NewRow_tb = '0' then
               write(row, v_data_write(8191 downto 8191 - BottomLimit_tb));
               NewRow_tb     <= '1';
               RowCounter_tb <= RowCounter_tb + 1;

            else
               writeline(file_handler, row);
               NewRow_tb <= '0';

               OutputState_tb <= "11";

            end if;

         elsif OutputState_tb <= "11" then
            --Check if all 256 samples have been written
            if RowCounter_tb < 256 then
               OutputState_tb <= "01";

            else
               OutputState_tb <= "00";

            end if;

         elsif OutputState_tb = "00" then
            report "I am done!";
            AllDone <= '1';
            file_close(file_handler);

            
         end if;

         if reset_tb = '1' then

            --Tesbench signals initial values
            InputState_tb            <= "01";
            OutputState_tb           <= "01";
            CreateInput_tb           <= (others => '0');
            InputCounter_tb          <= 0;
            ResidualsCalculatedIn_tb <= '0';

            --LoadData initial values
            DatablockOut_tb      <= (others => '0');
            DataBlockReadyOut_tb <= '0';

            CurrentValue_tb  <= (others => '0');
            SampleCounter_tb <= 0;
            MicCounter_tb    <= 0;
            InputCounter_tb  <= 0;

            EndOfFileReached_tb <= '0';

            --SaveToFile initial values
            NewRow_tb      <= '0';
            AllDone        <= '0';
            RowCounter_tb  <= 0;
            BottomLimit_tb <= 0;
            DataSavedIn_tb <= '0';
            LengthError <= '0';

            --AdjacentResidual initial values
            DataBlockIn_tb      <= (others => '0');
            ReadyToEncodeIn_tb  <= '0';
            DataBlockReadyIn_tb <= '0';
            ReadyToReciveIn_tb  <= '0';

            --kCalculator initial values
            ResidualValueIn_tb            <= (others => '0');
            NewDataIn_tb                  <= '0';
            ReadyToEncodeInkCalculator_tb <= '0';

            --RiceEncode initial values
            AllResidualsIn_tb          <= (others => '0');
            kValueIn_tb                <= "01000";
            NewKIn_tb                  <= '0';
            NewResidualsIn_tb          <= '0';
            ReadytoReciveCodeWordIn_tb <= '0';

            --CodeWordAssembler initial values
            CodeWordIn_tb         <= (others => '0');
            CodeWordLenIn_tb      <= (others => '0');
            k_valueIn_tb          <= "01000";
            NewCodeWordReadyIn_tb <= '0';
            DataSavedIn_tb        <= '0';

            --in the else statement inputs for entitys that are driven by outputs from other entitys are specified
         else

            --LoadData
            ResidualsCalculatedIn_tb <= ResidualsCalculatedOut_tb;

            --AdjacentResidual
            ReadyToEncodeIn_tb  <= ReadyToEncode_tb;
            ReadyToReciveIn_tb  <= ReadyToReciveOut_tb;
            DataBlockIn_tb      <= DatablockOut_tb;
            DataBlockReadyIn_tb <= DataBlockReadyOut_tb;

            --kCalculator
            ResidualValueIn_tb            <= ResidualValueOut_tb;
            NewDataIn_tb                  <= NewDataOut_tb;
            ReadyToEncodeInkCalculator_tb <= ReadyToEncode_tb;

            --RiceEncode
            AllResidualsIn_tb          <= AllResidualsOut_tb;
            kValueIn_tb                <= kValueOut_tb;
            NewKIn_tb                  <= NewKOut_tb;
            NewResidualsIn_tb          <= NewResidualOut_tb;
            ReadytoReciveCodeWordIn_tb <= ReadyToReciveCodeWordOut_tb;

            --CodeWordAssembler
            CodeWordIn_tb         <= CodeWord_tb;
            CodeWordLenIn_tb      <= CodeWordLen_tb;
            k_valueIn_tb          <= k_valueOut_tb;
            NewCodeWordReadyIn_tb <= NewCodeWordReady_tb;

         end if;

      end if;
   end process;

   main_1234 : process
   begin
      test_runner_setup(runner, runner_cfg);
      while test_suite loop
         if run("wave") then
            -- test 1 is so far only meant for gktwave

            --wait for 2950000ns; -- duration for a full datablock
            --wait for 30000 ns;

            wait until AllDone = '1' for 3 ms;
            assert AllDone = '1' report"AllDone should be set HIGH" severity failure;

         elsif run("auto") then

            wait for 11 ns;

         end if;
      end loop;

      test_runner_cleanup(runner);
   end process;

   test_runner_watchdog(runner, 100 ms);
end architecture;