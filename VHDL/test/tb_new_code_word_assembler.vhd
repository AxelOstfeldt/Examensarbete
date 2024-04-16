library IEEE;
use IEEE.STD_LOGIC_1164.all;
use ieee.numeric_std.all;

library vunit_lib;
context vunit_lib.vunit_context;

use work.MATRIX_TYPE.all;

entity tb_new_code_word_assembler is
   generic (
      runner_cfg : string
   );

end tb_new_code_word_assembler;

architecture new_code_word_assembler_arch of tb_new_code_word_assembler is

   constant C_CLK_CYKLE      : time      := 8 ns; -- 125 MHz
   signal clk_tb             : std_logic := '0';
   signal reset_tb           : std_logic := '1';
   signal StateDelay_tb      : std_logic_vector(2 downto 0);
   signal CodeWordCreator_tb : std_logic_vector(12 downto 0);

   signal CodeWordIn_tb         : std_logic_vector(1023 downto 0);--CodeWord
   signal CodeWordLenIn_tb      : std_logic_vector(9 downto 0);
   signal k_valueIn_tb          : std_logic_vector(4 downto 0);--Saved as metadata
   signal NewCodeWordReadyIn_tb : std_logic;--New codeword available for assemble
   signal DataSavedIn_tb        : std_logic;

   signal AllCodeWordsOut_tb          : std_logic_vector(8191 downto 0);--All codewords together, length is 2^13 - 1
   signal AssembleDoneOut_tb          : std_logic;--New CodeWord ready to be sent
   signal ReadyToReciveCodeWordOut_tb : std_logic;

   signal ErrorOut_tb : std_logic;--Send an error signal when error state is reached
begin
   clk_tb <= not(clk_tb) after C_CLK_CYKLE/2;

   reset_tb <= '1', '0' after 35 ns;

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

         ErrorOut => ErrorOut_tb
      );

   ws_process_1234 : process (clk_tb)
   begin

      if falling_edge(clk_tb) then

         if StateDelay_tb = "001" then
            CodeWordCreator_tb <= std_logic_vector(unsigned(CodeWordCreator_tb) - 4);
            StateDelay_tb      <= "010";
            NewCodeWordReadyIn_tb   <= '0';

         elsif StateDelay_tb = "010" then
            --set the codeword input
--            CodeWordIn_tb(1023)             <= CodeWordCreator_tb(12);
--            CodeWordIn_tb(1022)             <= CodeWordCreator_tb(11);
--            CodeWordIn_tb(1021)             <= CodeWordCreator_tb(10);
--            CodeWordIn_tb(1020)             <= CodeWordCreator_tb(9);
--            CodeWordIn_tb(1019)             <= CodeWordCreator_tb(8);
--            CodeWordIn_tb(1018)             <= CodeWordCreator_tb(7);
--            CodeWordIn_tb(1017)             <= CodeWordCreator_tb(6);
--            CodeWordIn_tb(1016)             <= CodeWordCreator_tb(5);
--            CodeWordIn_tb(1015)             <= CodeWordCreator_tb(4);
--            CodeWordIn_tb(1014)             <= CodeWordCreator_tb(3);
--            CodeWordIn_tb(1013)             <= CodeWordCreator_tb(2);
--            CodeWordIn_tb(1012)             <= CodeWordCreator_tb(1);
--            CodeWordIn_tb(1011)             <= CodeWordCreator_tb(0);
            CodeWordIn_tb(1010)             <= '1';
            codewordIn_tb(1023 downto 1011) <= codewordcreator_tb(12 downto 0);
            NewCodeWordReadyIn_tb              <= '0';
            StateDelay_tb                 <= "011";

         elsif StateDelay_tb = "011" then

            NewCodeWordReadyIn_tb <= '1';

            StateDelay_tb <= "100";

         elsif StateDelay_tb = "100" then
            NewCodeWordReadyIn_tb <= '0';

            StateDelay_tb <= "000";

         elsif StateDelay_tb = "101" then
            if AssembleDoneOut_tb = '1' then
               DataSavedIn_tb <= '1';

            else
               StateDelay_tb <= "001";
               DataSavedIn_tb <= '0';

            end if;


         else

            if AssembleDoneOut_tb = '1' then


               if to_integer(unsigned(k_valueIn_tb)) < 31 then
                  k_valueIn_tb <= std_logic_vector(unsigned(k_valueIn_tb) + 1);

               else
                  k_valueIn_tb <= "01000";--start at 8

               end if;

               StateDelay_tb <= "101";

            elsif ReadyToReciveCodeWordOut_tb = '1' then
               StateDelay_tb <= "001";
            end if;

            
            NewCodeWordReadyIn_tb <= '0';

         end if;


         if reset_tb = '1' then
            StateDelay_tb      <= "001";
            CodeWordCreator_tb <= (others => '1');
            CodeWordIn_tb        <= (others => '0');
            NewCodeWordreadyIn_tb   <= '0';
            CodeWordLenIn_tb <= std_logic_vector(to_unsigned(13,10));
            k_valueIn_tb         <= "01000";--start at 8
            DataSavedIn_tb <= '0';
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