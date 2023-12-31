var xpath = '//div[@class="bn-table-container"]//table//tr[@data-row-key]'
var result = document.evaluate(xpath, document, null, XPathResult.ANY_TYPE, null);
// result.iterateNext()
for (const c in result) {
    console.log('c')
}
return {"a":"123","b":456}


// 典型目标
// <tr data-row-key="0_ETCUSDT_BOTH" class="bn-table-row bn-table-row-level-0" style="cursor: default;">
// <td class="bn-table-cell"><div class="css-1493auf"><div data-bn-type="text" class=" css-1c82c04">ETCUSDT<div data-bn-type="text" class="css-ebwo6x">永续</div></div><div class="css-1et76yp">3x</div></div></td>
// <td class="bn-table-cell"><div class="css-13n52y">267.33 ETC</div></td>
// <td class="bn-table-cell">22.560</td>
// <td class="bn-table-cell">22.589</td>
// <td class="bn-table-cell">2,012.87 USDT<br>(全仓)</td>
// <td class="bn-table-cell"><div data-bn-type="text" class="css-1f23r63">+7.59 USDT</div><div data-bn-type="text" class="css-1f23r63">(+0.38%)</div></td>
// </tr>