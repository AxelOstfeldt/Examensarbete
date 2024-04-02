-- Copyright (C) 2018  Intel Corporation. All rights reserved.
-- Your use of Intel Corporation's design tools, logic functions 
-- and other software and tools, and its AMPP partner logic 
-- functions, and any output files from any of the foregoing 
-- (including device programming or simulation files), and any 
-- associated documentation or information are expressly subject 
-- to the terms and conditions of the Intel Program License 
-- Subscription Agreement, the Intel Quartus Prime License Agreement,
-- the Intel FPGA IP License Agreement, or other applicable license
-- agreement, including, without limitation, that your use is for
-- the sole purpose of programming logic devices manufactured by
-- Intel and sold by Intel or its authorized distributors.  Please
-- refer to the applicable agreement for further details.

-- ***************************************************************************
-- This file contains a Vhdl test bench template that is freely editable to   
-- suit user's needs .Comments are provided in each section to help the user  
-- fill out necessary details.                                                
-- ***************************************************************************
-- Generated on "04/02/2024 22:26:30"
                                                            
-- Vhdl Test Bench template for design  :  Adjacent
-- 
-- Simulation tool : ModelSim-Altera (VHDL)
-- 

LIBRARY ieee;                                               
USE ieee.std_logic_1164.all;                                

ENTITY Adjacent_vhd_tst IS
END Adjacent_vhd_tst;
ARCHITECTURE Adjacent_arch OF Adjacent_vhd_tst IS
-- constants                                                 
-- signals                                                   
SIGNAL clk : STD_LOGIC;
SIGNAL original_value : STD_LOGIC_VECTOR(23 DOWNTO 0);
SIGNAL recrated_value : STD_LOGIC_VECTOR(23 DOWNTO 0);
COMPONENT Adjacent
	PORT (
	clk : IN STD_LOGIC;
	original_value : OUT STD_LOGIC_VECTOR(23 DOWNTO 0);
	recrated_value : OUT STD_LOGIC_VECTOR(23 DOWNTO 0)
	);
END COMPONENT;
BEGIN
	i1 : Adjacent
	PORT MAP (
-- list connections between master ports and signals
	clk => clk,
	original_value => original_value,
	recrated_value => recrated_value
	);
init : PROCESS                                               
-- variable declarations                                     
BEGIN                                                        
        -- code that executes only once
		clk <= '1';
		wait for 50 ns;
		clk <= '0'
		wait for 50 ns;

		  
WAIT;                                                       
END PROCESS init;                                           
always : PROCESS                                              
-- optional sensitivity list                                  
-- (        )                                                 
-- variable declarations                                      
BEGIN                                                         
        -- code executes for every event on sensitivity list  
WAIT;                                                        
END PROCESS always;                                          
END Adjacent_arch;
