from typing import List, Any, Callable

class CellUtils:
    @staticmethod
    def map_cells(cells: List[List['Cell']], callback: Callable[['Cell'], Any]) -> List[List[Any]]:
        results = []

        for row in cells:
            row_results = []
            for cell in row:
                result = callback(cell)
                row_results.append(result)
            results.append(row_results)

        return results


    @staticmethod
    def reduce_cells(cells: List[List['Cell']], callback: Callable[[Any, 'Cell'], Any], initial_value: Any) -> Any:
        result = initial_value

        for row in cells:
            for cell in row:
                result = callback(result, cell)

        return result


    @staticmethod
    def filter_cells(cells: List[List['Cell']], callback: Callable[['Cell'], bool]) -> List[List['Cell']]:
        results = []

        for row in cells:
            row_results = []
            for cell in row:
                if callback(cell):
                    row_results.append(cell)
            results.append(row_results)

        return results
