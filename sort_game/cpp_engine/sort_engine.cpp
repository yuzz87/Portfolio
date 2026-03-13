#include <algorithm>
#include <chrono>
#include <iostream>
#include <random>
#include <string>
#include <vector>

#include "algorithms/algorithms.h"

namespace {

bool tryParseInt(const char* value, int& out) {
    try {
        out = std::stoi(value);
        return true;
    } catch (...) {
        return false;
    }
}

std::vector<int> createShuffledArray(int size, bool hasSeed, unsigned int seed) {
    std::vector<int> values(size);

    for (int i = 0; i < size; ++i) {
        values[i] = i + 1;
    }

    std::mt19937 rng;
    if (hasSeed) {
        rng.seed(seed);
    } else {
        std::random_device rd;
        rng.seed(rd());
    }

    std::shuffle(values.begin(), values.end(), rng);
    return values;
}

bool executeSort(const std::string& algorithm, std::vector<int>& values) {
    if (algorithm == "bubble") {
        bubbleSort(values);
        return true;
    }

    if (algorithm == "selection") {
        selectionSort(values);
        return true;
    }

    if (algorithm == "insertion") {
        insertionSort(values);
        return true;
    }

    if (algorithm == "merge") {
        mergeSort(values);
        return true;
    }

    if (algorithm == "quick") {
        quickSort(values);
        return true;
    }

    if (algorithm == "heap") {
        heapSort(values);
        return true;
    }

    return false;
}

}  // namespace

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: sort_engine <algorithm> <size> [seed]\n";
        return 2;
    }

    const std::string algorithm = argv[1];

    int size = 0;
    if (!tryParseInt(argv[2], size) || size <= 0) {
        std::cerr << "Invalid size\n";
        return 2;
    }

    bool hasSeed = false;
    unsigned int seed = 0;

    if (argc >= 4) {
        int parsedSeed = 0;
        if (!tryParseInt(argv[3], parsedSeed) || parsedSeed < 0) {
            std::cerr << "Invalid seed\n";
            return 2;
        }

        hasSeed = true;
        seed = static_cast<unsigned int>(parsedSeed);
    }

    std::vector<int> values = createShuffledArray(size, hasSeed, seed);

    // 計測対象はソート処理そのものだけにする
    const auto start = std::chrono::high_resolution_clock::now();
    const bool executed = executeSort(algorithm, values);
    const auto end = std::chrono::high_resolution_clock::now();

    if (!executed) {
        std::cerr << "Unknown algorithm\n";
        return 2;
    }

    const double durationMs =
        std::chrono::duration<double, std::milli>(end - start).count();

    std::cout << "{";
    std::cout << "\"algorithm\":\"" << algorithm << "\",";
    std::cout << "\"size\":" << size << ",";
    std::cout << "\"seed\":" << seed << ",";
    std::cout << "\"duration_ms\":" << durationMs;
    std::cout << "}\n";

    return 0;
}