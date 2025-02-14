let { CH552T, .. } = import "fak/mcus.ncl" in
let {ColToRowKey, RowToColKey} = import "fak/keyboard.ncl" in

let side_central = {
    mcu = CH552T,
    matrix = {
        cols = [16, 17],
        rows = [32, 15, 12, 13]
    },
    split.channel = CH552T.features.uart_30_31,
} in

let side_periph = {
    mcu = CH552T,
    matrix = {
        cols = [16, 17],
        rows = [32, 15, 12, 13]
    },
    split.channel = CH552T.features.uart_30_31,
    keys = 
        let C = ColToRowKey in
        let R = RowToColKey in
        [
            C 0 0, R 0 1, C 0 2, R 0 3, R 3 3,
            C 1 0, R 1 1, C 1 2, R 1 3, R 2 3,
            C 2 0, R 2 1, C 2 2, C 3 2,
            C 3 0, R 3 1,
        ],
} in

side_central & {
    usb_dev = {
        vendor_id = 21681 #0x54B1
        product_id = 1,
        product_ver = 46193 #0xB471 Kazhan means bat ^^
    },
    split.peripheral = side_periph,
    keys = 
        let C = ColToRowKey in
        let R = RowToColKey in
        let S = PeripheralSideKey in
        [
            C 3 0, C 0 0, R 0 1, C 0 2, R 0 3,      S 0,  S 1,  S 2,  S 3,  S 4,
            C 2 0, C 1 0, R 1 1, C 1 2, R 1 3,      S 5,  S 6,  S 7,  S 8,  S 9,
                   R 3 1, R 2 1, C 2 2, R 2 3,      S 10, S 11, S 12, S 13,
                                 C 3 2, R 3 3,      S 14, S 15
        ],
}