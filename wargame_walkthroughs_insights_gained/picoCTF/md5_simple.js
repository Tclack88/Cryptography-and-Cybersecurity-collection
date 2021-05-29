var top_list = ['f49bf}', '_again_e', 'this', 'Password\x20Verified', 'Incorrect\x20password', 'getElementById', 'value', 'substring', 'picoCTF{', 'not_this'];
            (function(array1, index1) {
                var var1 = function(index2) {
                    while (--index2) {
                        array1['push'](array1['shift']());
                    }
                };
                var1(++index1);
            }(top_list, 0x1b3));
            var var2 = function(number1, unused) {
                var var3 = top_list[number1];
                return var3;
            };
            function verify() {
                checkpass = document[var2('0x0')]('pass')[var2('0x1')];
                if (checkpass[var2('0x2')](0, 8) == var2('0x3')) {
                    if (checkpass[var2('0x2')](7, 9) == '{n') {
                        if (checkpass[var2('0x2')](8, 16) == var2('0x4')) {
                            if (checkpass[var2('0x2')](3, 6) == 'oCT') {
                                if (checkpass[var2('0x2')](24, 32) == var2('0x5')) {
                                    if (checkpass['substring'](6, 11) == 'F{not') {
                                        if (checkpass[var2('0x2')](16, 24) == var2('0x6')) {
                                            if (checkpass[var2('0x2')](12, 16) == var2('0x7')) {
                                                alert(var2('0x8'));
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else {
                    alert(var2('0x9'));
                }
            }



