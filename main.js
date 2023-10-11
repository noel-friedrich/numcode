const numInput = document.getElementById("numinput")
const visibleNumInput = document.getElementById("visible_numinput")
const analyseButton = document.getElementById("analysebutton")
const errorOutput = document.getElementById("erroroutput")
const resultOutput = document.getElementById("resultoutput")

function click(n) {
    if (numInput.value.length >= 8) {
        return
    }

    let number = parseInt(n)
    numInput.value += number
    numInput.oninput()
}

function undoInput() {
    numInput.value = numInput.value.slice(0, numInput.value.length - 1)
    numInput.oninput()
}

function resetInput() {
    numInput.value = ""
    numInput.oninput()
}

function updateVisibleInput() {
    let numbers = Array.from(numInput.value)
    let out = ""
    for (let i = 0; i < 8; i++) {
        out += numbers[i] ?? "-"
        if (i != 7) {
            out += " "
        }
    }
    visibleNumInput.value = out
}

numInput.oninput = () => {
    const setError = (msg, correct=false) => {
        errorOutput.textContent = msg
        analyseButton.disabled = !correct
        updateVisibleInput()
    }

    const num = numInput.value.toString()

    if (!num)
        return setError("")

    if (!/^[0-9]*$/.test(num))
        return setError("Please only use numbers (0-9)")

    if (num.length < 8 || num.length > 8)
        return setError("")

    return setError("", true)
}