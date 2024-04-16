library IEEE;
use IEEE.STD_LOGIC_1164.all;
use ieee.numeric_std.all;

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

   signal ErrorOut_CodeWordAssmbler_tb : std_logic;

   --Signals used in testbench
   signal StateDelay_tb   : std_logic_vector(1 downto 0);
   signal CreateInput_tb  : std_logic_vector(23 downto 0);
   signal InputCounter_tb : integer range 0 to 1535;

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

         ErrorOut => ErrorOut_CodeWordAssmbler_tb
      );
   ws_process_12345 : process (clk_tb)
   begin

      if falling_edge(clk_tb) then

         if StateDelay_tb = "01" then

            --set input values for testbench
            DataBlockIn_tb(1535 - InputCounter_tb) <= CreateInput_tb(23);
            DataBlockIn_tb(1534 - InputCounter_tb) <= CreateInput_tb(22);
            DataBlockIn_tb(1533 - InputCounter_tb) <= CreateInput_tb(21);
            DataBlockIn_tb(1532 - InputCounter_tb) <= CreateInput_tb(20);
            DataBlockIn_tb(1531 - InputCounter_tb) <= CreateInput_tb(19);
            DataBlockIn_tb(1530 - InputCounter_tb) <= CreateInput_tb(18);
            DataBlockIn_tb(1529 - InputCounter_tb) <= CreateInput_tb(17);
            DataBlockIn_tb(1528 - InputCounter_tb) <= CreateInput_tb(16);
            DataBlockIn_tb(1527 - InputCounter_tb) <= CreateInput_tb(15);
            DataBlockIn_tb(1526 - InputCounter_tb) <= CreateInput_tb(14);
            DataBlockIn_tb(1525 - InputCounter_tb) <= CreateInput_tb(13);
            DataBlockIn_tb(1524 - InputCounter_tb) <= CreateInput_tb(12);
            DataBlockIn_tb(1523 - InputCounter_tb) <= CreateInput_tb(11);
            DataBlockIn_tb(1522 - InputCounter_tb) <= CreateInput_tb(10);
            DataBlockIn_tb(1521 - InputCounter_tb) <= CreateInput_tb(9);
            DataBlockIn_tb(1520 - InputCounter_tb) <= CreateInput_tb(8);
            DataBlockIn_tb(1519 - InputCounter_tb) <= CreateInput_tb(7);
            DataBlockIn_tb(1518 - InputCounter_tb) <= CreateInput_tb(6);
            DataBlockIn_tb(1517 - InputCounter_tb) <= CreateInput_tb(5);
            DataBlockIn_tb(1516 - InputCounter_tb) <= CreateInput_tb(4);
            DataBlockIn_tb(1515 - InputCounter_tb) <= CreateInput_tb(3);
            DataBlockIn_tb(1514 - InputCounter_tb) <= CreateInput_tb(2);
            DataBlockIn_tb(1513 - InputCounter_tb) <= CreateInput_tb(1);
            DataBlockIn_tb(1512 - InputCounter_tb) <= CreateInput_tb(0);

            --Increament Create Input
            CreateInput_tb <= std_logic_vector(signed(CreateInput_tb) + 1);
            --24*62 = 1488, so when 1488 this state is in its second to last lap and adds 24 more to pass the if statement limit
            if InputCounter_tb > 1488 then
               StateDelay_tb <= "00";

            else
               --increment InputCounter_tb to set the nxt 24 values for the next mic
               InputCounter_tb     <= InputCounter_tb + 24;
               DataBlockReadyIn_tb <= '0';

            end if;

         elsif StateDelay_tb = "10" then
            --this state reset the CreateInput_tb and InputCounter_tb
            InputCounter_tb <= 0;

            if CreateInput_tb(23) = '0' then
               CreateInput_tb <= "111111111111110111111111";

            else
               CreateInput_tb <= "000000000000000010000000";

            end if;

            if ResidualsCalculatedOut_tb = '0' then
               DataBlockReadyIn_tb <= '0';
               StateDelay_tb <= "00";

            else
               DataBlockReadyIn_tb <= '1';
               
            end if;

         elsif StateDelay_tb = "11" then
            --This stated is entered Once the full codeword is assembled and ready to be sent
            --This indicated that the codeword can be saved and the next assemble can start
            DataSavedIn_tb <= '1';

            if AssembleDoneOut_tb = '0' then
               StateDelay_tb <= "00";
               DataSavedIn_tb <= '0';

            else
               DataSavedIn_tb <= '1';
               

            end if;



         else
            DataBlockReadyIn_tb <= '0';
            DataSavedIn_tb <= '0';

            if ResidualsCalculatedOut_tb = '1' then
               StateDelay_tb <= "10";
            
            elsif AssembleDoneOut_tb = '1' then
               StateDelay_tb <= "11";
               

            end if;
            --DataSavedIn_tb        <= DataSavedOut_tb; MÅSTE FIXAS

         end if;

         if reset_tb = '1' then

            --Tesbench signals initial values
            StateDelay_tb   <= "01";
            CreateInput_tb  <= (others => '0');
            InputCounter_tb <= 0;
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
            --AdjacentResidual
            ReadyToEncodeIn_tb <= ReadyToEncode_tb;
            ReadyToReciveIn_tb <= ReadyToReciveOut_tb;

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

            wait for 50000 ns; -- duration of test 1

         elsif run("auto") then

            wait for 11 ns;

         end if;
      end loop;

      test_runner_cleanup(runner);
   end process;

   test_runner_watchdog(runner, 100 ms);
end architecture;