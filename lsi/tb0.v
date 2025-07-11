`timescale 1ns/1ps

module comp_tb;

  reg [3:0] a, b;
  wire a_gt_b, a_eq_b, a_lt_b;

  comparator uut (
    .a(a),
    .b(b),
    .a_gt_b(a_gt_b),
    .a_eq_b(a_eq_b),
    .a_lt_b(a_lt_b)
  );

  initial begin
    $dumpfile("62100186_kadai0.vcd");
    $dumpvars(0, comp_tb);

    a = 4'd3; b = 4'd5; #10;
    a=4'd8; b=4'd2; #10;
    a=4'd7; b=4'd7; #10;
    a=4'd15; b=4'd14; #10;
    a=4'd0; b=4'd1; #10;
    a=4'd9; b=4'd9; #10;

    $finish;
  end

endmodule

