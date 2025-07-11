`timescale 1ns / 1ps

module alu_4bit_tb;

  reg[3:0] a;
  reg[3:0] b;
  reg[2:0] s;
  wire [3:0] y;

  alu_4bit uut (
    .a(a),
    .b(b),
    .s(s),
    .y(y)
  );

  initial begin
    $dumpfile("62100186_kadai1.vcd");
    $dumpvars(0, alu_4bit_tb);

    s = 3'b000; a = 4'b0000; b = 4'b0000;

    s = 3'b000; a = 4'b1000; b = 4'b0110; #10;
    s = 3'b001; a = 4'b0110; b = 4'b1010; #10;
    s = 3'b010; a = 4'b1001; b = 4'b0011; #10;
    s = 3'b011; a = 4'b1100; b = 4'b0111; #10;
    s = 3'b100; a = 4'b0011; b = 4'b0000; #10;
    s = 3'b101; a = 4'b1010; b = 4'b1111; #10;
    s = 3'b110; a = 4'b1100; b = 4'b0110; #10;
    s = 3'b111; a = 4'b0111; b = 4'b0010; #10;

    $finish;
  end

endmodule
