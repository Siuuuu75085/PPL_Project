grammar chatbox;

program: conditionalCommand|command;

command: addProduct | deleteProduct | increaseAmount | decreaseAmount | setAmount | listProducts | viewCart | checkOut | applyDiscount;
conditionalCommand: IF condition THEN command;
condition: totalValue|itemAmount;

totalValue: 'total is' compareWords MONEY;
itemAmount: 'amount of' NAME 'is' compareWords QUANTITY;

compareWords: ('equal to' | 'more than' | 'less than' | 'not equal to' | 'greater than or equal to' | 'less than or equal to');
addProduct: ADD QUANTITY NAME (',' QUANTITY NAME)* ('to cart')?;
deleteProduct: DELETE NAME (',' QUANTITY NAME)* ('from cart')?;
increaseAmount: INCREASE NAME ('by')? QUANTITY;
decreaseAmount: DECREASE NAME ('by')? QUANTITY;
setAmount: SET NAME 'to' QUANTITY;
applyDiscount: 'apply' DISCOUNT;
listProducts: 'list' ('all products' | NAME);
viewCart: 'view cart';
checkOut: 'check out';

ADD: 'add';
DELETE: 'delete';
INCREASE: 'increase';
DECREASE: 'decrease';
SET: 'set';
IF: 'if';
THEN: 'then';
DISCOUNT: ('welcome'|'goodbye'|'see you soon');

NAME: [a-zA-Z][a-zA-Z]*;
QUANTITY: [0-9]+;
TIME: [0-9][0-9]':'[0-9][0-9];
MONEY: [0-9]+'.'[0-9][0-9];

WS: [ \t\r\n]+ -> skip;

// noname4now