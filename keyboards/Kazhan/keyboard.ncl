let { CH552T, .. } = import "fak/mcus.ncl" in
let {ColToRowKey, RowToColKey} = import "fak/keyboard.ncl" in

let side_central = {
    mcu = CH552T,
    matrix = {

    },
    split.channel = CH552T.features.uart_12_13,
} in

let side_periph = {
    mcu = CH552T,
    matrix = {

    },
    split.channel = CH552T.features.uart_30_31,
    keys = 
        let C = ColToRowKey in
        let R = RowToColKey in
        [
            
        ]

} in

side_central & {

}