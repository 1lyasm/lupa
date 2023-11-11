function runAlgorithm() {
    var selectedAlgorithm = document.getElementById("algorithm").value;
    var selectedDataset = document.getElementById("dataset").value;

    // You can replace this with your actual algorithm logic
    var result = "Running " + selectedAlgorithm + " on " + selectedDataset + "...";

    document.getElementById("result").innerText = result;
}

