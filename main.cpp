#include <cassert>
#include <cmath>
#include <iostream>
#include <vector>

class PageRank {
    public:
  std::vector<double> pageRank(std::vector<std::vector<double>> Graph,
                               int IterationCount, double DampingFactor) {
    int NodeCount = Graph.size();
    double DampingTerm = (1.0 - DampingFactor) / NodeCount;
    double InitialValue = 1.0 / NodeCount;
    std::vector<double> PageRankValues(NodeCount, InitialValue);
    std::vector<int> OutgoingWeights = computeOutgoingWeights(Graph, NodeCount);
    for (int IterationCounter = 0; IterationCounter < IterationCount;
         ++IterationCounter) {
      std::vector<double> OldValues = PageRankValues;
      for (int NodeIndex = 0; NodeIndex < NodeCount; ++NodeIndex) {
        PageRankValues[NodeIndex] = updatePageRankValue(
            PageRankValues, NodeIndex, Graph, NodeCount, OldValues, DampingTerm,
            OutgoingWeights, DampingFactor);
      }
      std::cout << "pageRank: values: ";
      printVector<double>(PageRankValues);
      assertClose(sumVector(PageRankValues), 1.0000000);
    }
    return PageRankValues;
  }

  double sumVector(std::vector<double> Vector) {
    double Sum = 0.0;
    for (const auto &Value : Vector)
      Sum += Value;
    return Sum;
  }

  std::vector<int>
  computeOutgoingWeights(std::vector<std::vector<double>> Graph,
                         int NodeCount) {
    std::vector<int> OutgoingWeights(NodeCount, 0);
    for (int ColumnNodeIndex = 0; ColumnNodeIndex < NodeCount;
         ++ColumnNodeIndex) {
      int OutgoingWeight = 0;
      for (int RowNodeIndex = 0; RowNodeIndex < NodeCount; ++RowNodeIndex) {
        OutgoingWeight +=
            static_cast<int>(std::ceil(Graph[RowNodeIndex][ColumnNodeIndex]));
      }
      OutgoingWeights[ColumnNodeIndex] = OutgoingWeight;
    }
    printVector<int>(OutgoingWeights);
    return OutgoingWeights;
  }

  inline double
  updatePageRankValue(std::vector<double> UpdatedValues, int NodeIndex,
                      std::vector<std::vector<double>> Graph, int NodeCount,
                      std::vector<double> OldValues, double DampingTerm,
                      std::vector<int> OutgoingWeights, double DampingFactor) {
    double UpdateValue = DampingTerm;
    double PageRankSum = 0;
    for (int OtherNodeIndex = 0; OtherNodeIndex < NodeCount; ++OtherNodeIndex) {
      if (OtherNodeIndex == NodeIndex)
        continue;
      if (std::ceil(Graph[NodeIndex][OtherNodeIndex]) == 1) {
        PageRankSum +=
            OldValues[OtherNodeIndex] / OutgoingWeights[OtherNodeIndex];
      }
    }
    double result = UpdateValue + DampingFactor * PageRankSum;
    std::cout << "updateVal: result: " << result << "\n";
    return result;
  }

  void assertCloseVector(std::vector<double> Vector1,
                         std::vector<double> Vector2, int Length) {
    double Threshold = 0.000001;
    for (int I = 0; I < Length; ++I)
      assert(std::fabs(Vector1[I] - Vector2[I]) <= Threshold);
  }

  void assertClose(double Value1, double Value2) {
    double Threshold = 0.000001;
    assert(std::fabs(Value1 - Value2) <= Threshold);
  }

  template <typename T> void printVector(std::vector<T> Vector) {
    for (const auto &Value : Vector)
      std::cout << Value << " ";
    std::cout << "\n";
  }

  void test() {
    std::cout << "Testing PageRank: ";
    std::vector<std::vector<double>> Graph = {{0, 0, 0, 0, 1},
                                              {0.5, 0, 0, 0, 0},
                                              {0.5, 0, 0, 0, 0},
                                              {0, 1, 0.5, 0, 0},
                                              {0, 0, 0.5, 1, 0}};
    int IterationCount = 100;
    double DampingFactor = 0.85;
    std::vector<double> Output = pageRank(Graph, IterationCount, DampingFactor);
    std::vector<double> Expected = {0.25419178, 0.13803151, 0.13803151,
                                    0.20599017, 0.26375504};
    printVector<double>(Output);
    printVector<double>(Expected);
    int ExpectedLength = Expected.size();
    int OutputLength = Output.size();
    assert(OutputLength == ExpectedLength);
    assertCloseVector(Output, Expected, ExpectedLength);
    std::cout << "PASSED";
  }
};

int main() {
    auto pr = PageRank();
    pr.test();
}

