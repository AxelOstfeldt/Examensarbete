library IEEE;
use IEEE.STD_LOGIC_1164.all;
use ieee.numeric_std.all;
use std.textio.all;

library vunit_lib;
context vunit_lib.vunit_context;

use work.MATRIX_TYPE.all;

entity tb_load_data is--Testbench file name here
   generic (
      runner_cfg : string
   );

end tb_load_data;

architecture load_data_arch of tb_load_data is--Testbench file name here
   --General signals
   constant C_SCK_CYKLE : time      := 8 ns; -- 125 MHz
   signal clk_tb        : std_logic := '0';
   signal reset_tb      : std_logic := '1';

   signal CurrentValue_tb  : std_logic_vector(23 downto 0);
   signal StateDelay_tb    : std_logic_vector(1 downto 0);
   signal SampleCounter_tb : integer range 0 to 65535;
   signal MicCounter_tb    : integer range 0 to 65535;
   signal InputCounter_tb  : integer range 0 to 1535;

   --Signals to/from AdjacentResiduals
   signal DatablockOut_tb          : std_logic_vector(1535 downto 0);
   signal DataBlockReadyOut_tb     : std_logic;
   signal ResidualsCalculatedIn_tb : std_logic;

   --singals that helo with plotting
   signal LastMicReached_tb   : std_logic;
   signal EndOfFileReached_tb : std_logic;

begin
   clk_tb <= not(clk_tb) after C_SCK_CYKLE/2;--testbench clock

   reset_tb <= '1', '0' after 35 ns;
   ws_process_1234 : process (clk_tb)
      variable text_line : line;
      variable row_value : std_logic_vector(23 downto 0);
      --Make sure this directiory is correct!
      --file my_file : text open read_mode is "/home/toad/Projects/FPGA-sampling2/pl/test/first_sample_binary.txt";
      --file my_file : text open read_mode is "/home/toad/Projects/FPGA-sampling2/pl/test/data_block_binary.txt";
      file my_file : text open read_mode is "C:\\Users\\axelo\\OneDrive\\Skrivbord\\Exjobb\\GIT\\SoundData\\VHDL\\data_block_binary.txt";
   begin
      --test code
      if falling_edge(clk_tb) then

         if StateDelay_tb = "01" then
            LastMicReached_tb <= '0';

            --check that it is not end of file
            if not endfile(my_file) then
               --point to the next line
               readline(my_file, text_line);
               --read the current lint
               read(text_line, row_value);

               StateDelay_tb <= "10";


            else
               --StateDelay_tb       <= "00";
               EndOfFileReached_tb <= '1';

            end if;

         elsif StateDelay_tb = "10" then
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
               StateDelay_tb <= "01";

            else
               StateDelay_tb <= "00";

               --Set DataBlockReadyOut_tb to high to indicate that the datablock is done
               DataBlockReadyOut_tb <= '1';

            end if;

         else
            --if ResidualsCalculatedIn_tb is high AdjacentResiduals have recived the datablock
            --a new datablock can therefore be read from the text file

            if ResidualsCalculatedIn_tb = '1' then
               if MicCounter_tb = 63 then
                  --increment the sample counter to indicate that the next sample is going to be encoded
                  SampleCounter_tb <= SampleCounter_tb + 1;

                  LastMicReached_tb <= '1';
                  --reset the mic counter, so that the new datablock starts at mic 0
                  MicCounter_tb <= 0;

               elsif MicCounter_tb = 0 then
                  --by setting the first clock cykle with ResidualsCalculatedIn_tb as high to be used for reseting MicCounter
                  --it ensures that ResidualCalculated can read the Residualsbeffor reseting them

                  CurrentValue_tb      <= (others => '0');
                  DataBlockOut_tb      <= (others => '0');
                  DataBlockReadyOut_tb <= '0';
                  InputCounter_tb      <= 0;

                  --if all 256 samples have been read the test is done
                  --else the next sample is grabbed for all mics
                  if SampleCounter_tb < 256 then
                     StateDelay_tb <= "01";

                  end if;

               end if;

            end if;
         end if;

         if reset_tb = '1' then
            CurrentValue_tb  <= (others => '0');
            DataBlockOut_tb  <= (others => '0');
            StateDelay_tb    <= "00";
            MicCounter_tb    <= 0;
            SampleCounter_tb <= 0;

            EndOfFileReached_tb      <= '0';
            LastMicReached_tb        <= '0';
            DataBlockReadyOut_tb     <= '0';
            ResidualsCalculatedIn_tb <= '1';


         end if;
      end if;

   end process;

   main_1234 : process
   begin
      test_runner_setup(runner, runner_cfg);
      while test_suite loop
         if run("wave") then
            -- test 1 is so far only meant for gktwave

            wait for 300000 ns; -- duration of test 1

         elsif run("auto") then

            wait for 11 ns;

         end if;
      end loop;

      test_runner_cleanup(runner);
   end process;

   test_runner_watchdog(runner, 100 ms);
end architecture;