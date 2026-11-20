
# Parallel API Pricing




## Summary

| API | Pricing (USD) | Timing & processing |
| - | - | - |
| **Search** Pages and excerpts for latency-sensitive queries | **\$1–\$5** / 1,000 requests Includes 10 results per request. Additional results: \$1 / 1,000. [Mode pricing →](#search-api) | **200 ms–3 s** Synchronous Reasoning: n/a |
| **Image Search** Images from across the web | **\$1–\$5** / 1,000 requests Up to 20 results per request. [Mode pricing →](#image-search-api) | **1–3 s** Synchronous Reasoning: n/a |
| **Place Search** Local businesses and points of interest | **\$1–\$5** / 1,000 requests Up to 20 results per request. [Mode pricing →](#place-search-api) | **1–5 s** Synchronous Reasoning: n/a |
| **Extract** Retrieve page content | **\$1** / 1,000 URLs | **1–20 s** Synchronous Reasoning: n/a |
| **Decisions** Typed answers grounded in web evidence | **\$1** / 1,000 requests Up to 100 questions per request. | **200 ms–1 s** Synchronous Reasoning: n/a |
| **Task** Deep research, enrichment and custom research | **\$5–\$2,400** / 1,000 successful runs One charge per run, regardless of output fields. [Processor pricing →](#task-api) | **10 s–2 hr** Asynchronous Reasoning: low to high |
| **Responses** Answers grounded in live web research (OpenAI-compatible) | **\$10–\$250** / 1,000 successful requests [Reasoning tier pricing →](#responses-api) | **5–60 s** Synchronous Reasoning: low to high |
| **Monitor** Always-on web monitoring | **\$3–\$10** / 1,000 checks Each execution counts as one check. [Processor pricing →](#monitor-api) | **Ongoing** Asynchronous Reasoning: low |
| **FindAll** Build verified lists and databases | **\$0.25** / run + **\$0.03** / match Base tier Enrichment billed separately. [All tiers & preview pricing →](#findall-api) | **10 s–2 hr** Asynchronous Reasoning: low to high |
| **Entity Search** Find people and companies | **\$5** / 1,000 requests Includes 100 results per request. Additional results: \$0.05 / 1,000. | **1–3 s** Synchronous Reasoning: n/a |

## Web Tools

### Search API

By default, the Search API returns 10 page results and their excerpts per request. Pricing varies by [mode](https://docs.parallel.ai/search/modes.md). Excerpt length doesn't affect the price.

| Component | Cost (\$/1000) |
| - | - |
| Per 1,000 `turbo` or `fast` requests (default 10 results) | 1 |
| Per 1,000 `basic` or `advanced` requests (default 10 results) | 5 |
| Per 1,000 results beyond the first 10 in a request | 1 |

**Cost formula (`turbo` / `fast`):**

$$
\text{total cost} = 0.001 + (0.001 \times \text{results beyond the first 10})
$$

**Cost formula (`basic` / `advanced`):**

$$
\text{total cost} = 0.005 + (0.001 \times \text{results beyond the first 10})
$$

### Image Search API

Image Search is priced per request. Pricing varies by [mode](https://docs.parallel.ai/image-search/modes.md), and each request can return up to 20 results at no additional cost.

| Component | Cost (\$/1000) |
| - | - |
| Per 1,000 `fast` requests | 1 |
| Per 1,000 `advanced` requests | 5 |

### Place Search API

Place Search is priced per request. Pricing varies by [mode](https://docs.parallel.ai/place-search/modes.md), and each request can return up to 20 results at no additional cost.

| Component | Cost (\$/1000) |
| - | - |
| Per 1,000 `fast` requests | 1 |
| Per 1,000 `advanced` requests | 5 |

### Extract API

| Component | Cost (\$/1000) |
| - | - |
| Per 1,000 URLs | 1 |

### Decisions API

The [Parallel Decisions API](https://docs.parallel.ai/decisions/decisions-quickstart.md) is priced per request, with up to 100 questions included in each call.

| Component | Cost (\$/1000) |
| - | - |
| Per 1,000 `fast` requests | 1 |

## Web Agents

### Task API

Task API pricing is based on the [processor](https://docs.parallel.ai/task-api/guides/choose-a-processor.md) you select. Cost is per 1,000 Task Runs.

| Processor | Cost (\$/1000) | Latency | Strengths |
| - | - | - | - |
| `lite` | 5 | 10s - 60s | Basic metadata, fallback, low latency |
| `base` | 10 | 15s - 100s | Reliable standard enrichments |
| `core` | 25 | 60s - 5min | Cross-referenced, moderately complex outputs |
| `core2x` | 50 | 60s - 10min | High complexity cross referenced outputs |
| `pro` | 100 | 2min - 10min | Exploratory web research |
| `ultra` | 300 | 5min - 25min | Advanced multi-source deep research |
| `ultra2x` | 600 | 5min - 50min | Difficult deep research |
| `ultra4x` | 1200 | 5min - 90min | Very difficult deep research |
| `ultra8x` | 2400 | 5min - 2hr | The most difficult deep research |

> [!NOTE]
>
> Pricing is per Task Run (row), not per output field (cell). A single Task Run can populate many output fields—whether you request 1 field or 20 fields, the cost is the same.

> [!NOTE]
>
> You are only charged for successfully completed runs. Failed runs are not billed.

### Responses API

[Responses API](https://docs.parallel.ai/responses-api/responses-quickstart.md) pricing is based on the `reasoning.effort` tier you select. Cost is per 1,000 requests. You are only charged for successful responses.

| Reasoning effort | Cost (\$/1000) | Latency | Designed for |
| - | - | - | - |
| `low` | 10 | \~5-10s | Simple fact-retrieval questions |
| `medium` (default) | 50 | \~15-20s | Multi-hop fact-retrieval questions |
| `high` | 250 | \~30-60s | Deep-research questions requiring extensive search and synthesis |

### Monitor API

Monitor requests are priced per execution on a per-thousand (CPM) basis. Choose a processor based on query scope; both tiers deduplicate and reason over results.

| Processor | Cost (\$/1000) | Best for |
| - | - | - |
| `lite` | 3 | Narrow queries — a single entity, domain, or signal type |
| `base` | 10 | Wide queries — entity classes, topic areas, regions |

**Cost formula:**

$$
\text{total cost} = \text{cost per 1,000} \times \text{number of executions} / 1000
$$

### FindAll API

FindAll API pricing is based on the [generator](https://docs.parallel.ai/findall-api/core-concepts/findall-generator-pricing.md) you select, with a fixed cost plus a per-match cost.

| Generator | Fixed Cost | Per Match | Best For |
| - | - | - | - |
| `preview` | \$0.10 | \$0.00 | Testing queries (\~10 candidates) |
| `base` | \$0.25 | \$0.03 | Broad, common queries where you expect many matches |
| `core` | \$2.00 | \$0.15 | Specific queries with moderate expected matches |
| `pro` | \$10.00 | \$1.00 | Highly specific queries with rare or hard-to-find matches |

**Cost formula:**

$$
\text{total cost} = \text{fixed cost} + (\text{cost per match} \times \text{\# matches})
$$

If you add [enrichments](https://docs.parallel.ai/findall-api/features/findall-enrich.md), each enrichment adds its own per-match cost based on the Task API processor you choose (see Task API pricing above).

#### Entity Search

[Entity Search](https://docs.parallel.ai/findall-api/entity-search.md) is a fast, synchronous people-and-company search, the real-time counterpart to FindAll. It is priced per request, including 100 results by default.

| Component | Cost (\$/1000) |
| - | - |
| Per 1,000 requests (default 100 results) | 5 |
| Per 1,000 additional results | 0.05 |

**Cost formula:**

$$
\text{total cost} = 0.005 + (0.00005 \times \text{additional results})
$$
