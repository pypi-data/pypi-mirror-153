from ..core import runCMD, strInList


def start_neo4j():
    if neo4j_available():
        return True
    run_result, run_err = runCMD("neo4j start", output_type="REALTIME_RETURN")
    if neo4j_available():
        return True
    else:
        return False


def stop_neo4j():
    if not neo4j_available():
        return True
    run_result, run_err = runCMD("neo4j stop", output_type="REALTIME_RETURN")
    if neo4j_available():
        return False
    else:
        return True


def neo4j_available():
    run_result, run_err = runCMD("neo4j status", output_type="REALTIME_RETURN")
    if strInList("Neo4j is running", run_result):
        return True
    elif strInList("Neo4j is not running", run_result):
        return False
