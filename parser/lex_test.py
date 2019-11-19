from c_lex import lexer

ipt = """
int main()
{
    int a = 0x1;
    a += 1;
    printf("Hello World!");
    return 0;
}
"""

lexer.input(ipt)

while True:
    token = lexer.token()
    if not token: break
    print(token)
