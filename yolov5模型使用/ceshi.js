data = [
{
"co": {
"update_at": "2023-04-10 17:21:12",
"unit": "",
"id": "co",
"unit_symbol": "",
"current_value": "Cwarn",
"at": "2023-04-10 17:21:12",
"value": "Cwarn"
},
"yw": {
"update_at": "2023-04-10 17:21:09",
"unit": "",
"id": "yw",
"unit_symbol": "",
"current_value": "Sok",
"at": "2023-04-10 17:21:09",
"value": "Sok"
}
}
]

// // 遍历对象
// for (let obj of data) {
//   // 遍历obj对象中的属性
//   for (let key in obj) {
//     // 取出value的值
//     let value = obj[key].value;
//     console.log(value);
//   }
// }

let coValue = data[0].co.value;
let ywValue = data[0].yw.value;

console.log(coValue); // 输出："Cwarn"
console.log(ywValue); // 输出："Sok"




