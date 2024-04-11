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
   signal StateDelay_tb      : std_logic_vector(1 downto 0);
   signal CodeWordCreator_tb : std_logic_vector(12 downto 0);

   signal CodeWord_tb       : std_logic_vector(1023 downto 0);--CodeWord
   signal CodeWordLength_tb : std_logic_vector(9 downto 0);
   signal k_value_tb        : std_logic_vector(4 downto 0);--Saved as metadata
   signal NewCodeWordIn_tb  : std_logic;--New codeword available for assemble

   signal ReadyToRecive_tb      : std_logic;
   signal AssembleDone_tb       : std_logic;--New CodeWord ready to be sent
   signal ErrorOut_tb           : std_logic;--Send an error signal when error state is reached
   signal AllCodeWords_tb       : std_logic_vector(8191 downto 0);--All codewords together, length is 2^13 - 1
   signal AllCodeWordsLength_tb : std_logic_vector(12 downto 0);--Count the total length of used bits in "AllCodeWords"

begin
   clk_tb <= not(clk_tb) after C_CLK_CYKLE/2;

   reset_tb <= '1', '0' after 35 ns;

   TestCodeWordAssembler : entity work.CodeWordAssembler
      port map(
         reset              => reset_tb,
         clk                => clk_tb,
         CodeWord           => CodeWord_tb,
         CodeWordLength     => CodeWordLength_tb,
         k_value            => k_value_tb,
         NewCodeWordIn      => NewCodeWordIn_tb,
         AssembleDone       => AssembleDone_tb,
         ErrorOut           => ErrorOut_tb,
         AllCodeWords       => AllCodeWords_tb,
         AllCodeWordsLength => AllCodeWordsLength_tb,
         ReadyToRecive      => ReadyToRecive_tb
      );

   ws_process_1234 : process (clk_tb)
   begin

      if falling_edge(clk_tb) then

         if StateDelay_tb = "01" then
            CodeWordCreator_tb <= std_logic_vector(unsigned(CodeWordCreator_tb) - 4);
            StateDelay_tb      <= "10";
            NewCodeWordIn_tb   <= '0';

         elsif StateDelay_tb = "10" then
            --set the codeword input
            CodeWord_tb(1023) <= CodeWordCreator_tb(12);
            CodeWord_tb(1022) <= CodeWordCreator_tb(11);
            CodeWord_tb(1021) <= CodeWordCreator_tb(10);
            CodeWord_tb(1020) <= CodeWordCreator_tb(9);
            CodeWord_tb(1019) <= CodeWordCreator_tb(8);
            CodeWord_tb(1018) <= CodeWordCreator_tb(7);
            CodeWord_tb(1017) <= CodeWordCreator_tb(6);
            CodeWord_tb(1016) <= CodeWordCreator_tb(5);
            CodeWord_tb(1015) <= CodeWordCreator_tb(4);
            CodeWord_tb(1014) <= CodeWordCreator_tb(3);
            CodeWord_tb(1013) <= CodeWordCreator_tb(2);
            CodeWord_tb(1012) <= CodeWordCreator_tb(1);
            CodeWord_tb(1011) <= CodeWordCreator_tb(0);
            CodeWord_tb(1010) <= '1';

            if AssembleDone_tb = '1' then

               if to_integer(unsigned(k_value_tb)) < 31 then
                  k_value_tb <= std_logic_vector(unsigned(k_value_tb) + 1);

               else
                  k_value_tb <= "01000";--start at 8

               end if;
            end if;

            NewCodeWordIn_tb <= '0';
            StateDelay_tb    <= "11";

         elsif StateDelay_tb = "11" then
            NewCodeWordIn_tb <= '1';

            StateDelay_tb <= "00";

         else
            if ReadyToRecive_tb = '1' then
               StateDelay_tb    <= "01";
               NewCodeWordIn_tb <= '0';

            end if;

         end if;
         if reset_tb = '1' then
            StateDelay_tb      <= "01";
            CodeWordCreator_tb <= (others => '1');
            CodeWord_tb        <= (others => '0');
            CodeWordLength_tb  <= std_logic_vector(to_unsigned(13, 10));--codeword length is 13, since that is the length of "CodeWordCreator_tb"
            NewCodeWordIn_tb   <= '0';
            k_value_tb         <= "01000";--start at 8
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