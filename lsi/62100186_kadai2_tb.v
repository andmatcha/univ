`timescale 1ns/1ps

module alu_5bit_tb;

  reg [4:0] a, b;
  reg [3:0] s;
  wire [4:0] y;

  alu_5bit uut (
    .a(a),
    .b(b),
    .s(s),
    .y(y)
  );

  initial begin
    $dumpfile("62100186_kadai2.vcd");
    $dumpvars(0, alu_5bit_tb);

    a = 5'h07; b = 5'h03; s = 4'h0; #10;
    a = 5'h03; b = 5'h08; s = 4'h1; #10;
    a = 5'h15; b = 5'h13; s = 4'h2; #10;
    a = 5'h01; b = 5'h0C; s = 4'h3; #10;
    a = 5'h12; b = 5'h05; s = 4'h4; #10;
    a = 5'h0A; b = 5'h0A; s = 4'h5; #10;
    a = 5'h0F; b = 5'h00; s = 4'h6; #10;
    a = 5'h00; b = 5'h04; s = 4'h7; #10;
    a = 5'h19; b = 5'h15; s = 4'h8; #10;
    a = 5'h05; b = 5'h0C; s = 4'h9; #10;
    a = 5'h06; b = 5'h00; s = 4'hA; #10;
    a = 5'h09; b = 5'h00; s = 4'hB; #10;
    a = 5'h19; b = 5'h0A; s = 4'hC; #10;
    a = 5'h00; b = 5'h15; s = 4'hD; #10;
    a = 5'h16; b = 5'h00; s = 4'hE; #10;
    a = 5'h12; b = 5'h0D; s = 4'hF; #10;

    $finish;
  end

endmodule
