module alu_4bit (
    input [3:0] a,
    input [3:0] b,
    input [2:0] s,
    output reg [3:0] y
);

always @(*) begin
    case (s)
        3'b000: y = b;
        3'b001: y = a << 1;
        3'b010: y = a | b;
        3'b011: y = a - b;
        3'b100: y = a ^ b;
        3'b101: y = a > b;
        3'b110: y = a & b;
        3'b111: y = a + b;
        default: y = 4'd0;
    endcase
end

endmodule
