module alu_5bit (
    input [4:0] a,
    input [4:0] b,
    input [3:0] s,
    output reg [4:0] y
);

always @(*) begin
    case (s)
        4'h0:  y = a + b;
        4'h1:  y = (b >> 1) + a;
        4'h2:  y = a & b;
        4'h3:  y = ~b;
        4'h4:  y = a ^ b;
        4'h5:  y = a == b;
        4'h6:  y = a ~^ b;
        4'h7:  y = b << 1;
        4'h8:  y = a ^ b;
        4'h9:  y = b - a;
        4'hA:  y = ~a;
        4'hB:  y = a | b;
        4'hC:  y = a < b;
        4'hD:  y = b;
        4'hE:  y = a >> 1;
        4'hF:  y = a > b;
        default: y = 5'd0;
    endcase
end

endmodule
