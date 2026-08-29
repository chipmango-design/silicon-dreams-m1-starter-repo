/*
 * Copyright (c) 2025 Pat Deegan
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

// All output pins must be assigned. If not used, assign to 0.
  assign uio_out = 0;
  assign uio_oe  = 0;


  wire [3:0] floor;
  wire [3:0] requested_floor;
    
 
  // List all unused inputs to prevent warnings
  wire _unused = &{ena, uio_in[7:0], 1'b0};
    
    bit_position_to_value b_pos(
        .bit_in(ui_in),
        .bit_out(requested_floor)
    );

  elevator_state_machine em (
    .clk(clk),
    .rst_n(rst_n),
    .requested_floor(requested_floor),
    //.requested_floor(4'd3),
    .current_floor(floor),
    .idle_display (uo_out [7])
  );
  
  segment7 s7 (
    .floor(floor),
    .segment(uo_out[6:0])
  );
  
endmodule


module elevator_state_machine (
  input clk, // Clock signal
  input rst_n, // Reset signal inverted
  input wire [3:0] requested_floor,
  output reg [3:0] current_floor,
  output reg idle_display 
);

  // Define the states
  parameter IDLE_STATE = 2'b00;
  parameter MOVING_UP = 2'b10;
  parameter MOVING_DOWN = 2'b11;
  parameter DUMMY_STATE = 2'b01;
  // parameter DELAY_COUNT = 32'd10000000;  // make longer for real hardware
  parameter DELAY_COUNT = 32'd10;  // make longer for real hardware
    
  // State register
  reg [1:0] current_state, next_state;
  reg [31:0] delay;

  // Combinational logic for next state and output
  always @(*) begin    
    case (current_state)
      IDLE_STATE, DUMMY_STATE: begin
       	idle_display = 1;
        if (current_floor < requested_floor)
          next_state = MOVING_UP;
        else if (current_floor > requested_floor)
          next_state = MOVING_DOWN;
        else
          next_state = IDLE_STATE;
      end
      MOVING_UP, MOVING_DOWN: begin
       	idle_display  = 0;
       if (current_floor < requested_floor)
            next_state = MOVING_UP;
       else if (current_floor > requested_floor)
           next_state = MOVING_DOWN;
       else 
          next_state = IDLE_STATE;
      end
      default:
        next_state = IDLE_STATE; // Error state, go back to IDLE
    endcase
  end
  
    // Sequential logic 
        always @(posedge clk or posedge rst_n) begin
            if ( rst_n ) begin
              current_state <= IDLE_STATE;
              current_floor <= 0;
              delay <= 0;
        end else begin
          current_state <= next_state; //Update the current state
            
          //Update the current_floor
          if (delay == DELAY_COUNT) begin
            delay <= 0; //Reset delay
            if (current_state == MOVING_UP) 
              current_floor <= current_floor + 1;
            else if (current_state == MOVING_DOWN) 
              current_floor <= current_floor - 1;
          end else 
             delay <= delay + 1;  //increment delay counter
        end
      end
endmodule


// 7-segment display

module segment7(
  input wire [3:0] floor, // 4 bit input to display digits < 10
  output reg [6:0] segment // 7 bit output for 7-segment display
);
  
    always @(*) begin
    case (floor)
      0: segment = 7'b0111111; 
      1: segment = 7'b0000110;
      2: segment = 7'b1011011;
      3: segment = 7'b1001111;
      4: segment = 7'b1100110; 
      5: segment = 7'b1101101;
      6: segment = 7'b1111101; 
      7: segment = 7'b0000111; 
      8: segment = 7'b1111111;
      9: segment = 7'b1101111;
      default: segment = 7'b0000000;
    endcase
  end
  
endmodule

module bit_position_to_value (
    input wire [7:0] bit_in,
    output reg [3:0] bit_out
);

    always @(*) begin
        case(bit_in)
            8'b00000000: bit_out = 0;
            8'b00000001: bit_out = 1;
            8'b00000010: bit_out = 2;
            8'b00000100: bit_out = 3;
            8'b00001000: bit_out = 4;
            8'b00010000: bit_out = 5;
            8'b00100000: bit_out = 6;
            8'b01000000: bit_out = 7;
            8'b10000000: bit_out = 8;
         default:
            bit_out = 0;
         endcase              
    end
endmodule
