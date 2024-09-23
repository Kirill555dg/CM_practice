import unittest
from unittest.mock import patch
from terminal import Terminal

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.terminal = Terminal("archive.tar", "log_file.xml", "start_script.txt")

    def test_ls1(self):
        output = sorted(self.terminal.ls([]).split())
        self.assertEqual(output, ['bin', 'files', 'users'])

    def test_ls2(self):
        output = sorted(self.terminal.ls(['users']).split())
        self.assertEqual(output, ['admin', 'user'])

    def test_ls3(self):
        output = sorted(self.terminal.ls(['files', 'users/user/home/fairy_tales']).split())
        self.assertEqual(output, ['Document.odt', 'Spreadsheet.ods', 'Text.txt', 'files:', 'users/user/home/fairy_tales:', 'Заяц.txt', 'Каша_из_топора.txt', 'Репка.txt'])

    def test_cd1(self):
        output = sorted(self.terminal.cd(['users/user/home/fairy_tales']).split())
        self.assertEqual(output, ['change', 'to', 'users/user/home/fairy_tales'])

    def test_cd2(self):
        output1 = self.terminal.cd(['users/user/home/'])
        output2 = self.terminal.cd([".."])
        output3 = self.terminal.cd([])
        output4 = self.terminal.cd(['bin/../files'])
        self.assertEqual(output1, "change to users/user/home")
        self.assertEqual(output2, "change to users/user")
        self.assertEqual(output3, "root directory")
        self.assertEqual(output4, "change to files")

    def test_cd3(self):
        output = self.terminal.cd(['users/user/home/', "qwe"])
        self.assertEqual(output, "cd: too many arguments")

    @patch('builtins.input', return_value='Some text for text')
    def test_rev1(self, mock):
        output1 = self.terminal.rev([])
        input = mock()
        self.assertEqual(output1, input[::-1])

    def test_rev2(self):
        output1 = self.terminal.rev(['files/Text.txt']).strip().split('\n')
        print("OUT1", output1)
        self.assertEqual(output1[0], "Some text for testing different commands"[::-1])
        self.assertEqual(output1[1], "Somebody once told me, the world is gonna roll me."[::-1])



    def test_find1(self):
        output = self.terminal.find([]).strip().split()
        answers = '''.
                     ./bin
                     ./files
                     ./files/Document.odt
                     ./files/Spreadsheet.ods
                     ./files/Text.txt
                     ./users
                     ./users/admin
                     ./users/admin/home
                     ./users/user
                     ./users/user/home
                     ./users/user/home/fairy_tales
                     ./users/user/home/fairy_tales/Заяц.txt
                     ./users/user/home/fairy_tales/Каша_из_топора.txt
                     ./users/user/home/fairy_tales/Репка.txt'''.strip().split()

        for i in range(len(answers)):
            self.assertEqual(output[i], answers[i])

    def test_find2(self):
        output = self.terminal.find(['users/admin']).strip().split()
        answers = '''users/admin
                     users/admin/home'''.strip().split()

        for i in range(len(answers)):
            self.assertEqual(output[i], answers[i])


    def test_find3(self):
        output = self.terminal.find(['files/Text.txt', 'bin/../bin']).strip().split()
        answers = '''files/Text.txt
                     bin/../bin'''.strip().split()

        for i in range(len(answers)):
            self.assertEqual(output[i], answers[i])

    def test_find4(self):
        output = self.terminal.find(['files/Text.txt/qwe', 'bin/../bin/smth']).strip().split('\n')
        answers = '''find: \'files/Text.txt/qwe\': No such file or directory\nfind: \'bin/../bin/smth\': No such file or directory'''.strip().split('\n')

        for i in range(len(answers)):
            self.assertEqual(output[i], answers[i])


    def test_date(self):
        output0 = self.terminal.date([])
        self.assertTrue(output0 != "")

        output1 = self.terminal.date(["10051440"]).strip()
        self.assertEqual(output1, "Sat Oct  5 14:40:00 2024")

        output2 = self.terminal.date(["10051430.25"]).strip()
        self.assertEqual(output2, "Sat Oct  5 14:30:25 2024")

        output3 = self.terminal.date(["1005143017.16"]).strip()
        self.assertEqual(output3, "Thu Oct  5 14:30:16 2017")

        output4 = self.terminal.date(["100514301917.16"]).strip()
        self.assertEqual(output4, "Fri Oct  5 14:30:16 1917")

        output5 = self.terminal.date(["100514301917.162"]).strip()
        self.assertEqual(output5, "date: invalid date ‘100514301917.162’")

        output6 = self.terminal.date(["13131313"]).strip()
        self.assertEqual(output6, "date: invalid date ‘13131313’")

    def test_parse_cmd(self):
        output1 = self.terminal.parse_cmd('exit')
        self.assertEqual(output1, 'exit')

if __name__ == '__main__':
    unittest.main()