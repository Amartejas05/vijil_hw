import asyncio
import aiohttp
import time
import statistics
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000/benchmark"
REQUESTS_PER_MINUTE = 60  # Example rate limit
REQUEST_INTERVAL = 60 / REQUESTS_PER_MINUTE

async def worker(session, tokens, results, rate_limiter):
    async with rate_limiter:
        async with session.get(API_URL, params={"tokens": tokens}) as response:
            result = await response.json()
            results.append({
                "tokens": result["tokens"],
                "latency": result["timestamp"] - start_time
            })

async def single_benchmark(num_workers, tokens):
    # runs multiple workers in parallel
    async with aiohttp.ClientSession() as session:
        results = []
        rate_limiter = asyncio.Semaphore(REQUESTS_PER_MINUTE)  # Rate limiting
        tasks = [worker(session, tokens, results, rate_limiter) for _ in range(num_workers)]
        await asyncio.gather(*tasks)
        return results

def analyze_results(results):
    latencies = [result["latency"] for result in results]
    tokens_per_second = sum([result["tokens"] for result in results]) / sum(latencies)
    
    analysis = {
        "average_tokens": statistics.mean([result["tokens"] for result in results]),
        "median_latency": statistics.median(latencies),
        "tokens_per_second": tokens_per_second
    }
    
    return analysis

def save_analysis_to_file(analysis, filename="benchmark_report.txt"):
    with open(filename, "w") as file:
        file.write("Benchmark Analysis:\n")
        file.write(f"Average Tokens: {analysis['average_tokens']}\n")
        file.write(f"Median Latency: {analysis['median_latency']}\n")
        file.write(f"Tokens Per Second: {analysis['tokens_per_second']}\n")

def create_chart(analysis, results, chart_filename="benchmark_chart.png"):
    plt.figure(figsize=(10, 6))
    
    latencies = [result["latency"] for result in results]

    # Latency distribution
    plt.subplot(2, 1, 1)
    plt.hist(latencies, bins=20, edgecolor='black')
    plt.title('Latency Distribution')
    plt.xlabel('Latency (seconds)')
    plt.ylabel('Frequency')
    
    # Tokens per second
    plt.subplot(2, 1, 2)
    plt.bar(['Tokens per Second'], [analysis["tokens_per_second"]])
    plt.ylabel('Tokens per Second')
    
    plt.tight_layout()
    plt.savefig(chart_filename)
    plt.close()

if __name__ == "__main__":
    num_workers = int(input("Enter the number of workers: "))
    tokens = int(input("Enter the number of tokens: "))

    start_time = time.time()
    results = asyncio.run(single_benchmark(num_workers, tokens))
    analysis = analyze_results(results)

    save_analysis_to_file(analysis)
    create_chart(analysis, results) # additional feature to visulaize the analysis
    
    print("Benchmark Analysis:")
    print(f"Average Tokens: {analysis['average_tokens']}")
    print(f"Median Latency: {analysis['median_latency']}")
    print(f"Tokens Per Second: {analysis['tokens_per_second']}")
