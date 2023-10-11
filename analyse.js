function isObviousPattern(number) {
    let uniqueNums = [...new Set(number.split(""))]
    if (uniqueNums.length <= 3)
        return true

    let obviousPatterns = [
        "1234", "2345", "3456", "4567",
        "5678", "6789", "2580", "12369",
        "14789"
    ]

    // add reversed versions
    obviousPatterns = obviousPatterns.concat(
        obviousPatterns.map(p => p.split("").reverse().join("")))
    
    for (let pattern of obviousPatterns) {
        if (number.includes(pattern)) {
            return true
        }
    }

    if (number.slice(0,4) == number.slice(4,8)) return true

    const countOccurences = (sub) => number.split(sub).length - 1
    if (countOccurences(number.slice(0, 3)) > 1) return true
    if (countOccurences(number.slice(1, 4)) > 1) return true
    if (countOccurences(number.slice(2, 5)) > 1) return true
    if (countOccurences(number.slice(3, 6)) > 1) return true
    if (countOccurences(number.slice(4, 7)) > 1) return true
    if (countOccurences(number.slice(5, 8)) > 1) return true

    return false
}

async function analyse(nums) {
    if (isObviousPattern(nums)) {
        console.log("Obvious Pattern")
        return [0, 1]
    }

    const inputs = Array.from({length: nums.length * 10}, () => 0)
    for (let i = 0; i < nums.length; i++) {
        inputs[i * 10 + parseInt(nums[i])] = 1
    }

    const session = new onnx.InferenceSession({
        backendHint: "cpu"
    })

    await session.loadModel("trained_network.onnx")
    const outputMap = await session.run([
        new onnx.Tensor(Float32Array.from(inputs), "float32")
    ])

    return Array.from(outputMap.get("out").data)
}

analyseButton.onclick = async () => {
    const nums = numInput.value

    let result = await analyse(nums)
    console.log(`result=[${result}]`)
    result = result.map(n => Math.round(n * 1000000) / 1000000)

    let output = `Result: I think your number (${numInput.value}) is actually randomly generated!`

    if (result[0] != 1 || result[1] != 0) {
        output = `Result: I think your number (${numInput.value}) is made up: I don't think it's randomly generated.`
    }

    resultOutput.textContent = output

    window.scrollTo({
        top: 9999,
        behavior: "smooth"
    })
}