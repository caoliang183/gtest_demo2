import argparse 
import os 
import random 
import subprocess 
import sys
import time
from datetime import datetime 
from pathlib import Path 
from concurrent.futures import ProcessPoolExecutor 
import re 
from typing import List, Tuple, Dict, Any, Set 
import xml.etree.ElementTree as ET 

DEBUG_MODE = False
#DEBUG_RUN = 20000
#DEBUG_MODE = True
#DEBUG_RUN = 200

def print_header(message: str):
    print(f"\n=== {message.upper()} ===")

import subprocess
import sys
import re
from typing import List, Tuple

def list_all_tests(test_executable: str) -> Tuple[List[Tuple[str, str, str]], int]:
    """列出所有测试用例（精确禁用检测），并返回去重后的结果
    
    Args:
        test_executable: 测试可执行文件路径
        
    Returns:
        Tuple[List[Tuple[str, str, str]], int]: 
            - 测试列表，每个元素是(suite, case, full_name)元组
            - 禁用的测试数量
    """
    command = f"{test_executable} --gtest_list_tests"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error listing tests: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    tests = []
    seen_tests = set()  # 用于去重的集合
    duplicate_tests = set()  # 新增：存储重复项 
    disabled = 0
    current_suite = ""
    
    for line in result.stdout.splitlines():
        if not line.strip(): 
            continue

        if not line.startswith("  "):  # 测试套件
            parts = line.split('#')
            current_suite = parts[0].rstrip('.')
            if current_suite.startswith("DISABLED_") or "/DISABLED_" in current_suite:
                disabled += 1
                current_suite = ""
        else:  # 测试用例
            if not current_suite: 
                disabled += 1
                continue
            test_case = re.sub(r'\s*#.*', '', line).strip()
            if test_case.startswith("DISABLED_") or "/DISABLED_" in test_case:
                disabled += 1
            elif test_case:
                full_name = f"{current_suite}.{test_case}"
                if full_name not in seen_tests:  # 检查是否已存在
                    seen_tests.add(full_name)
                    tests.append((current_suite, test_case, full_name))
                else:
                    duplicate_tests.add(full_name)  
 
    if duplicate_tests:
        print("\n[WARNING] Found duplicate test cases:")
        for dup in sorted(duplicate_tests):
            print(f"  - {dup}")
        print(f"Total duplicates: {len(duplicate_tests)}\n")
    print(f"Found {len(tests)} unique tests ({disabled} disabled)")
    return tests, disabled

def generate_partial_xml(xml_path: Path, log_file: Path):
    """从日志生成包含 passed/failed/skipped 测试的最小XML"""
    passed_tests = []
    failed_tests = []
    skipped_tests = []
    
    with open(log_file, "r") as f:
        for line in f:
            if "[       OK ]" in line:  # 提取通过的测试
                test_name = line.split("[       OK ]")[1].strip().split(" (")[0]
                passed_tests.append(test_name)
            elif "[  FAILED  ]" in line:  # 提取失败的测试
                test_name = line.split("[  FAILED  ]")[1].strip().split(" (")[0]
                failed_tests.append(test_name)
            elif "[  SKIPPED ]" in line:  # 提取跳过的测试
                test_name = line.split("[  SKIPPED ]")[1].strip().split(" (")[0]
                skipped_tests.append(test_name)
    
    # 生成最小XML结构
    root = ET.Element("testsuites")
    suite = ET.SubElement(
        root,
        "testsuite",
        name="PartialResults",
        tests=str(len(passed_tests) + len(failed_tests) + len(skipped_tests)),
        failures=str(len(failed_tests)),
        skipped=str(len(skipped_tests))
    )
    
    # 添加所有测试用例
    for test in passed_tests:
        ET.SubElement(suite, "testcase", name=test, status="run")
    for test in failed_tests:
        tc = ET.SubElement(suite, "testcase", name=test, status="run")
        ET.SubElement(tc, "failure", message="Test failed")
    for test in skipped_tests:
        tc = ET.SubElement(suite, "testcase", name=test, status="run")
        ET.SubElement(tc, "skipped")
    
    ET.ElementTree(root).write(xml_path, encoding="utf-8", xml_declaration=True)

def run_test_batch(batch: List[str], exe_path: str, repeat: int, 
                  timeout: int, log_dir: Path, job_id: int) -> bool:
    """执行测试批次（增强错误处理）"""
    filter_arg = ':'.join(batch)
    # 获取当前时间（精确到毫秒
    timestamp = str(time.time_ns()) 
    xml_path = log_dir / f"result_{timestamp}_{job_id}.xml"  
    cmd = [
        'powershell',
        '-Command',
        f'& "{exe_path}"',
        f'--gtest_repeat={repeat}',
        '--gtest_fail_fast',
        f'--gtest_filter="{filter_arg}"',
        f'--gtest_output=xml:"{xml_path}"'
    ]
    
    log_file = log_dir / f"job_{job_id}.log"
    print(f"\nStarting job {job_id} with {len(batch)} tests:")
    #print(f"  Command: {' '.join(cmd)}")
    print(f"  Log file: {log_file}")
    try:
        with open(log_file, "wb") as f:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
                #bufsize=1
            )
            
            while True:
                output = process.stdout.readline()
                if not output and process.poll() is not None:
                    break
                if output:
                    f.write(output)
                    f.flush()
                    decoded = output.decode('utf-8', errors='replace')
                    #print(decoded, end='', flush=True)  # 实时输出到控制台
            return_code = process.wait(timeout=timeout)
            if return_code != 0:
                print(f"Job {job_id} crashed with exit code {return_code}")
                if not xml_path.exists():
                    generate_partial_xml(xml_path, log_file)  # 生成部分结果
                return False
            return True
    except subprocess.TimeoutExpired:
        print(f"Job {job_id} timed out after {timeout}s")
        process.kill()
        if not xml_path.exists():
            generate_partial_xml(xml_path, log_file)  # 生成部分结果
        return False
    except Exception as e:
        print(f"Job {job_id} error: {str(e)}")
        if not xml_path.exists():
            generate_partial_xml(xml_path, log_file)  # 生成部分结果
        return False

def parse_gtest_xml(xml_path: Path) -> List[Dict[str, Any]]:
    """解析XML报告（增强容错）"""
    results = []
    try:
        with open(xml_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            if not content.strip():
                return []
                
            try:
                root = ET.fromstring(content)
                for testsuite in root.findall('testsuite'):
                    suite_name = testsuite.get('name')
                    for testcase in testsuite.findall('testcase'):
                        result = {
                            'suite': suite_name,
                            'name': testcase.get('name'),
                            'status': 'passed',
                            'time': testcase.get('time', '0'),
                            'message': None
                        }
                        if testcase.find('failure') is not None:
                            result['status'] = 'failed'
                            result['message'] = testcase.find('failure').get('message', '')
                        elif testcase.find('skipped') is not None:
                            result['status'] = 'skipped'
                        results.append(result)
            except ET.ParseError as e:
                print(f"XML parse error in {xml_path}: {str(e)}")
    except Exception as e:
        print(f"Error reading {xml_path}: {str(e)}")
    return results

from collections import defaultdict  # 添加这行导入

def write_summary(execution_state: Dict[str, Set[str]],
                 disabled: int,
                 suite_stats: Dict[str, Dict],
                 summary_file: str,
                 log_dir: Path,
                 start_time: float = None):
    """生成测试摘要报告（完整修正版）"""
    # 统计套件总数
    total_suites = len(suite_stats)
    failed_suites = sum(1 for s in suite_stats.values() if s['failed'] > 0)
    
    # 从执行状态获取基础统计
    total_tests = len(execution_state['all_tests'])
    passed = len(execution_state['passed'])
    failed = len(execution_state['failed'])
    skipped = len(execution_state['skipped'])
    
    # 验证完整性
    executed_total = passed + failed + skipped
    count_mismatch = executed_total != total_tests

    def format_time(seconds: float) -> str:
        return f"{seconds:.1f}s ({seconds/60:.2f}min)"
    
    # 计算时间统计
    total_time = sum(s['total_time'] for s in suite_stats.values())
    passed_time = sum(s['total_time'] * (s['passed'] / max(1, s['passed'] + s['failed'] + s['skipped'])) 
                   for s in suite_stats.values())
    failed_time = sum(s['total_time'] * (s['failed'] / max(1, s['passed'] + s['failed'] + s['skipped'])) 
                   for s in suite_stats.values())
    skipped_time = sum(s['total_time'] * (s['skipped'] / max(1, s['passed'] + s['failed'] + s['skipped'])) 
                   for s in suite_stats.values())

    # 按前缀分组套件
    prefix_groups = defaultdict(list)
    for suite_name, stats in suite_stats.items():
        prefix = suite_name.split('_')[0] + '_' if '_' in suite_name else 'Other'
        stats['name'] = suite_name
        prefix_groups[prefix].append(stats)

    # 准备套件统计数据（保持原有结构）
    suite_details = []
    for suite_name, stats in suite_stats.items():
        suite_total = stats['passed'] + stats['failed'] + stats['skipped']
        if suite_total == 0:
            continue
            
        suite_details.append({
            'name': suite_name,
            'total': suite_total,
            'passed': stats['passed'],
            'failed': stats['failed'],
            'skipped': stats['skipped'],
            'time': stats['total_time'],
            'passed_pct': stats['passed'] / suite_total * 100 if suite_total > 0 else 0,
            'failed_pct': stats['failed'] / suite_total * 100 if suite_total > 0 else 0,
            'skipped_pct': stats['skipped'] / suite_total * 100 if suite_total > 0 else 0
        })
    suite_details.sort(key=lambda x: x['name'].lower())

    # GitHub Summary (Markdown格式)
    with open(summary_file, "w", encoding="utf-8") as f:
        # 摘要部分
        f.write("## Test Execution Summary\n")
        if start_time:
            f.write(f"- Wall Clock Time: {format_time(time.time() - start_time)}\n")
        f.write(f"- Total Suites: {total_suites}\n")  # 新增套件总数
        f.write(f"- Total tests: {total_tests}\n")
        f.write(f"- Passed: {passed} ({passed/total_tests*100:.1f}%) - Time: {format_time(passed_time)}\n")
        f.write(f"- Failed: {failed} (in {failed_suites} suites, {failed/total_tests*100:.1f}%) - Time: {format_time(failed_time)}\n")  # 修正失败统计
        f.write(f"- Skipped: {skipped} ({skipped/total_tests*100:.1f}%) - Time: {format_time(skipped_time)}\n")
        f.write(f"- Disabled (Suite, Case): {disabled}\n")
        f.write(f"- Overall Time: {format_time(total_time)}\n")
        
        f.write("\n## Suite Group Summary\n")
        for prefix, suites in sorted(prefix_groups.items()):
            group_total = sum(s['passed']+s['failed']+s['skipped'] for s in suites)
            f.write(f"<details>\n<summary>{prefix.rstrip('_')} ({len(suites)} suites, {group_total} tests)</summary>\n\n")
            f.write("| Suite | Passed | Failed | Skipped | Time |\n")
            f.write("|-------|--------|--------|---------|------|\n")
            for suite in sorted(suites, key=lambda x: x['name']):
                s_total = suite['passed'] + suite['failed'] + suite['skipped']
                f.write(f"| {suite['name']} | "
                       f"{suite['passed']}({suite['passed']/s_total*100:.1f}%) | "
                       f"{suite['failed']}({suite['failed']/s_total*100:.1f}%) | "
                       f"{suite['skipped']}({suite['skipped']/s_total*100:.1f}%) | "
                       f"{format_time(suite['total_time'])} |\n")
            f.write("\n</details>\n")
        
        # 保持原有的详细套件统计
        f.write("\n## Detailed Suite Statistics\n")
        f.write("<details>\n<summary>Click to expand all suites</summary>\n\n")
        f.write("| Suite | Total | Passed | Failed | Skipped | Time |\n")
        f.write("|-------|-------|--------|--------|---------|------|\n")
        for suite in suite_details:
            f.write(f"| {suite['name']} | "
                   f"{suite['total']} | "
                   f"{suite['passed']}({suite['passed_pct']:.1f}%) | "
                   f"{suite['failed']}({suite['failed_pct']:.1f}%) | "
                   f"{suite['skipped']}({suite['skipped_pct']:.1f}%) | "
                   f"{format_time(suite['time'])} |\n")
        f.write("\n</details>\n")

        # 保持原有的失败详情

        # 失败详情（修正总数显示）
        if failed > 0:
            f.write("\n## Failed Tests Details\n")
            f.write("<summary><strong>Failed Tests Details {failed_suites} suites {failed} cases (Click to Expand)</strong></summary>\n\n")
            for suite, stats in sorted(suite_stats.items(), key=lambda x: x[0].lower()):
                if stats['failed'] > 0:
                    suite_total = stats['passed'] + stats['failed'] + stats['skipped']
                    f.write(f"- **{suite}**: {stats['passed']}/{suite_total} passed, {stats['failed']} failed\n")
                    seen_cases = set()
                    for case in stats['failed_cases']:
                        if case['name'] not in seen_cases:
                            f.write(f"  - `{case['name']}`: {case['error']}\n")
                            seen_cases.add(case['name'])
            f.write("\n</details>\n")

    # 终端输出（修正失败统计）
    print_header("test summary")
    if start_time:
        print(f"Wall Clock Time: {format_time(time.time() - start_time)}")
    print(f"Total Suites: {total_suites}")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed} ({passed/total_tests*100:.1f}%) - Time: {format_time(passed_time)}")
    print(f"Failed: {failed} (in {failed_suites} suites) - Time: {format_time(failed_time)}")  # 修正显示
    print(f"Skipped: {skipped} ({skipped/total_tests*100:.1f}%) - Time: {format_time(skipped_time)}")
    print(f"Disabled suite: {disabled}")
    print(f"Overall Time: {format_time(total_time)}")

    print("\nSuite Group Summary:")
    for prefix, suites in sorted(prefix_groups.items()):
        group_total = sum(s['passed']+s['failed']+s['skipped'] for s in suites)
        print(f"  {prefix.rstrip('_')}: {len(suites)} suites, {group_total} tests")

    # 保持原有的详细套件输出
    print("\nDetailed Suite Statistics:")
    print(f"{'Suite Name':<45} {'Passed':<10} {'Failed':<10} {'Skipped':<10} {'Time':<15}")
    for suite in suite_details:
        print(f"{suite['name'][:40]:<40}({suite['total']}) "
              f"{suite['passed']}({suite['passed_pct']:.1f}%){'':<2} "
              f"{suite['failed']}({suite['failed_pct']:.1f}%){'':<2} "
              f"{suite['skipped']}({suite['skipped_pct']:.1f}%){'':<2} "
              f"{format_time(suite['time'])}")
    

    # 本地日志文件（增强版）
    with open(log_dir / "summary.log", "w", encoding="utf-8") as f:
        f.write("TEST EXECUTION SUMMARY\n\n")
        if start_time:
            f.write(f"Wall Clock Time: {format_time(time.time() - start_time)}\n")
        f.write(f"Total Suites: {total_suites}\n")
        f.write(f"Total tests (expected): {total_tests}\n")
        f.write(f"Total tests (executed): {executed_total}\n")
        f.write(f"Passed: {passed} ({passed/total_tests*100:.1f}%)\n")
        f.write(f"Failed: {failed} (in {failed_suites} suites, {failed/total_tests*100:.1f}%)\n")
        f.write(f"Skipped: {skipped} ({skipped/total_tests*100:.1f}%)\n")
        f.write(f"Disabled: {disabled}\n")
        f.write(f"Total time: {format_time(total_time)}\n")
        if count_mismatch:
            f.write("\nWARNING: TEST COUNT MISMATCH!\n")
            f.write(f"Missing tests: {total_tests - executed_total}\n")
        
        # 新增：分组统计
        f.write("\nSUITE GROUP STATISTICS:\n")
        for prefix, suites in sorted(prefix_groups.items()):
            group_total = sum(s['passed']+s['failed']+s['skipped'] for s in suites)
            f.write(f"\n{prefix.rstrip('_')} ({len(suites)} suites, {group_total} tests):\n")
            for suite in sorted(suites, key=lambda x: x['name']):
                s_total = suite['passed'] + suite['failed'] + suite['skipped']
                f.write(f"  {suite['name']}: "
                       f"Passed={suite['passed']}({suite['passed']/s_total*100:.1f}%) "
                       f"Failed={suite['failed']}({suite['failed']/s_total*100:.1f}%) "
                       f"Skipped={suite['skipped']}({suite['skipped']/s_total*100:.1f}%)\n")
        
        # 保持原有的详细套件输出
        f.write("\nDETAILED SUITE STATISTICS:\n")
        for suite in suite_details:
            f.write(f"\n{suite['name']} (Total: {suite['total']}):\n")
            f.write(f"  Passed: {suite['passed']} ({suite['passed_pct']:.1f}%)\n")
            f.write(f"  Failed: {suite['failed']} ({suite['failed_pct']:.1f}%)\n")
            f.write(f"  Skipped: {suite['skipped']} ({suite['skipped_pct']:.1f}%)\n")
            f.write(f"  Time: {format_time(suite['time'])}\n")
        
        
        if failed > 0:
            f.write("\nFAILURE DETAILS:\n")
            f.write(f"Total failed suites: {failed_suites}\n")
            f.write(f"Total failed tests: {failed}\n")
            for suite, stats in suite_stats.items():
                if stats['failed'] > 0:
                    f.write(f"\n{suite}:\n")
                    for case in stats['failed_cases']:
                        f.write(f"  {case['name']}: {case['error']}\n")

    return failed > 0 or count_mismatch

def main():
    program_start = time.time() 
    parser = argparse.ArgumentParser()
    parser.add_argument("--exe", default="tests.exe")
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--timeout", nargs=3, type=int, default=[20,5,30])
    parser.add_argument("--jobs", nargs=3, type=int, default=[16,60,60])
    parser.add_argument("--batches", nargs=3, type=int, default=[256,32,1])
    parser.add_argument("--repeat", type=int, default=1)
    args = parser.parse_args()

    # 初始化执行状态
    execution_state = {
        'passed': set(),    # 已通过的测试
        'failed': set(),    # 当前失败的测试
        'skipped': set(),   # 跳过的测试
        'all_tests': set()  # 所有需要执行的测试
    }
    print(f"Running parameters: jobs={args.jobs}, batches={args.batches}")

    if DEBUG_MODE:
        args.jobs = [6, 2, 1]
        args.batches = [50, 20, 1]
        args.timeout = [60, 60, 60]
        print_header("debug mode active")
        print(f"Overriding parameters: jobs={args.jobs}, batches={args.batches}")

    exe_path = Path(args.exe).resolve()
    if not exe_path.exists():
        print(f"Error: Executable not found at {exe_path}", file=sys.stderr)
        sys.exit(1)
    test_cases, disabled = list_all_tests(args.exe)
    random.shuffle(test_cases)

    if 'DEBUG_RUN' in globals() and len(test_cases) > DEBUG_RUN:
        test_cases = test_cases[:DEBUG_RUN]
        print(f"Running first {len(test_cases)} tests only (DEBUG_RUN={DEBUG_RUN})")
    from collections import Counter 
    all_values = [t[2] for t in test_cases] 
 
    # 统计频率并筛选重复值 
    #for value in all_values:
    #    print(f"value: '{value}', length: {len(value)}, type: {type(value)}")
    value_counts = Counter(all_values)
    duplicates = [value for value, count in value_counts.items()  if count > 1]
 
    print("repeated:", duplicates)

    execution_state['all_tests'] = {t[2] for t in test_cases}
    remaining_tests = list(execution_state['all_tests'])

    # 准备日志目录
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    print(f"All logs will be saved in: {log_dir.absolute()}")
    for file in log_dir.glob("*"):  #for local repeat testing
        if file.is_file(): 
            file.unlink() 

    # 执行测试（多轮重试）
    has_crashes = False
    job_id_base = 0

    for retry in range(args.retries):
        if not remaining_tests:
            break

        round_start = "result_"+str(time.time_ns())+".xml"

        print_header(f"Trying {len(remaining_tests)} test cases {retry+1}/{args.retries} at {round_start}")
        current_batch_size = args.batches[retry]
        current_jobs = args.jobs[retry]
        # 初始化本轮失败记录
        failed_in_round = set()    

        try:
            # 分割测试批次
            test_batches = []
            for i in range(0, len(remaining_tests), current_batch_size):
                batch = remaining_tests[i:i + current_batch_size]
                test_batches.append(batch)

            # 执行批次（带超时处理）
            with ProcessPoolExecutor(max_workers=current_jobs) as pool:
                futures = {}
                for batch_idx, batch in enumerate(test_batches):
                    print_header(f"new job id: {job_id_base + batch_idx} ")
                    future = pool.submit(
                        run_test_batch, 
                        batch, 
                        str(exe_path), 
                        args.repeat,
                        args.timeout[retry] * 60, 
                        log_dir, 
                        job_id_base + batch_idx
                    )
                    futures[future] = batch

                # 处理结果
                for future in futures:
                    try:
                        if not future.result(timeout=args.timeout[retry] * 60 + 10):  # 额外10秒缓冲
                            failed_in_round.update(futures[future])
                    except subprocess.TimeoutExpired:
                        print(f"Batch timed out: {futures[future][:1]}...")
                        failed_in_round.update(futures[future])
                    except Exception as e:
                        print(f"Error processing batch: {str(e)}")
                        failed_in_round.update(futures[future])
                        has_crashes = True

            # 解析结果
            round_passed = 0
            round_skipped = 0
            round_failed = 0
            print(f"gtest result xml_file count: {len(list(log_dir.glob('result_*.xml')))}") 

            for xml_file in log_dir.glob("result_*.xml"):
                if xml_file.name < round_start: #previous run
                    print(f"processing xml_file (skip previoius ones): {xml_file} {xml_file.stat().st_size}")
                    continue
                print(f"processing xml_file: {xml_file} {xml_file.stat().st_size}")
                try:
                    if xml_file.exists():
                        for result in parse_gtest_xml(xml_file):
                            full_name = f"{result['suite']}.{result['name']}"
                            if full_name in execution_state['skipped']:
                                continue

                            if result['status'] == 'passed':
                                execution_state['passed'].add(full_name)
                                execution_state['failed'].discard(full_name)
                                round_passed += 1
                            elif result['status'] == 'failed':
                                execution_state['failed'].add(full_name)
                                round_failed += 1
                            elif result['status'] == 'skipped':
                                execution_state['skipped'].add(full_name)
                                round_skipped += 1
                except Exception as e:
                    print(f"Error parsing {xml_file}: {str(e)}")
                    has_crashes = True
        
            # 打印本轮统计
            print(f"\nRound {retry+1} Summary:")
            print(f"Tests Run: {len(remaining_tests)} (Total: {len(execution_state['all_tests'])})")
            print(f"   Passed: {round_passed} (Total: {len(execution_state['passed'])})")
            print(f"   Failed: {round_failed} (Total: {len(execution_state['failed'])})")
            print(f"  Skipped: {round_skipped} (Total: {len(execution_state['skipped'])})")
            print(f"  Round Total: {round_passed + round_failed + round_skipped}")
            # 准备下一轮
            remaining_tests = list(execution_state['failed']-execution_state['passed']-execution_state['skipped'])
            job_id_base = job_id_base + len(test_batches)

            print(f"preparing to re-run remaining {len(remaining_tests)} test cases starting from job {job_id_base}")

        except Exception as e:
            print(f"\nRound {retry+1} CRITICAL ERROR: {type(e).__name__}: {str(e)}")
            print("Traceback:", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            has_crashes = True
            # 尝试继续下一轮重试
            if retry < args.retries - 1:
                print_header(f"Tried {len(remaining_tests)} tests {retry+1}/{args.retries}")
                continue
            else:
                print("Maximum retries reached")
                break

# 收集所有结果（包括多次重试）
    all_results = []
    suite_stats = {}
    seen_keys = set()  # 使用 (suite, name) 元组作为唯一标识 
 
    for xml_file in log_dir.glob("result_*.xml"): 
        results = parse_gtest_xml(xml_file)
        for result in results:
            key = (result['suite'], result['name'])  # 复合键 
        
            if key not in seen_keys:
                seen_keys.add(key) 
                all_results.append(result) 
            else:
                print(f"repeated case in all xml: {key[0]}.{key[1]}")
        
        for result in results:
            suite = result['suite']
            if suite not in suite_stats:
                suite_stats[suite] = {
                    'passed': 0,
                    'failed': 0,
                    'skipped': 0,
                    'failed_cases': [],
                    'total_time': 0.0
                }
            
            suite_stats[suite][result['status']] += 1
            suite_stats[suite]['total_time'] += float(result.get('time', 0))
            
            if result['status'] == 'failed':
                suite_stats[suite]['failed_cases'].append({
                    'name': result['name'],
                    'error': result['message']
                })
    # 在收集结果后添加验证
    expected_count = min(DEBUG_RUN, len(test_cases)) if 'DEBUG_RUN' in globals() else len(test_cases)
    actual_count = len(all_results)
    
    if actual_count != expected_count:
        print(f"Warning: Expected {expected_count} results, got {actual_count}")
        print("Possible reasons:")
        print("1. Some tests didn't generate XML reports")
        print("2. Tests crashed before finishing")
        print("3. XML files were corrupted")

    # 最终验证和报告
    total_executed = (len(execution_state['passed']) + 
                     len(execution_state['failed']) + 
                     len(execution_state['skipped']))
    
    print(f"\nFinal Execution Report:")
    print(f"  Passed: {len(execution_state['passed'])}")
    print(f"  Failed: {len(execution_state['failed'])}")
    print(f"  Skipped: {len(execution_state['skipped'])}")
    print(f"  Total: {total_executed}")
    
    if total_executed != len(execution_state['all_tests']):
        missing = execution_state['all_tests'] - (
            execution_state['passed'] | 
            execution_state['failed'] | 
            execution_state['skipped']
        )
        print(f"\nWARNING: Missing {len(missing)} test executions!")
        with open(log_dir / "missing_tests.txt", "w") as f:
            f.write("\n".join(sorted(missing)[:1000]))

    has_failures = write_summary(
        execution_state=execution_state,
        disabled=disabled,
        suite_stats=suite_stats,
        summary_file=os.environ.get("GITHUB_STEP_SUMMARY", "summary.md"),
        log_dir=log_dir,
        start_time=program_start
    )

    if has_failures:
        print("\nERROR: Test run contains failures!")
        sys.exit(1)
    elif has_crashes:
        print("\nERROR: Test run contains missing executions!")
        sys.exit(1)
    else:
        print("\nSUCCESS: All tests executed successfully")
        sys.exit(0)
if __name__ == "__main__":
    main()