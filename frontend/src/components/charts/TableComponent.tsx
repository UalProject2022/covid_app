import { useMemo } from 'react';
import {
  AiOutlineArrowDown,
  AiOutlineArrowUp,
  AiOutlineDoubleLeft,
  AiOutlineDoubleRight,
  AiOutlineLeft,
  AiOutlineRight
} from 'react-icons/ai';
import { BsArrowDownUp } from 'react-icons/bs';
import {
  useFilters,
  useGlobalFilter,
  usePagination,
  useSortBy,
  useTable
} from 'react-table';
import BackToTop from '../ui/BackToTop';
import LoadingAnimation from '../ui/LoadingAnimation';
import TableColumnFilter from './TableColumnFilter';
import classes from './TableComponent.module.css';
import TableGlobalFilter from './TableGlobalFilter';


export function TableComponent(
  isLoading: boolean,
  data: any,
  setColumns: any,
  chartName: string,
) {
  const columns = useMemo(() => setColumns, []);
  const defaultColumn = useMemo(() => {
    return {
      Filter: TableColumnFilter,
    };
  }, []);

  const tableInstance = useTable(
    {
      columns: columns,
      data: data,
      defaultColumn,
      initialState: { pageSize: 25 },
    },
    useFilters,
    useGlobalFilter,
    useSortBy,
    usePagination
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    page,
    nextPage,
    previousPage,
    canNextPage,
    canPreviousPage,
    pageOptions,
    gotoPage,
    pageCount,
    setPageSize,
    prepareRow,
    state,
    setGlobalFilter,
  } = tableInstance;

  const { globalFilter, pageIndex, pageSize } = state;
  const chartElement = document.getElementById('tableDiv');
  chartElement?.scrollIntoView({ behavior: 'smooth' });

  function getColumnOrder(isSortedDesc: boolean | undefined) {
    if (isSortedDesc) {
      return <AiOutlineArrowDown size={20} />;
    } else {
      return <AiOutlineArrowUp size={20} />;
    }
  }

  return (
    <div className={classes.tableWrapper}>
      {isLoading ? (
        <div>
          <LoadingAnimation />
        </div>
      ) : (
        <>
          <div className={classes.title}>{chartName}</div>

          <div className={classes.divTable}>
            <TableGlobalFilter
              filter={globalFilter}
              setFilter={setGlobalFilter}
            />
            <table className={classes.table} {...getTableProps()}>
              <thead>
                {headerGroups.map((headerGroup) => (
                  <tr {...headerGroup.getHeaderGroupProps()}>
                    {headerGroup.headers.map((column) => (
                      <th
                        {...column.getHeaderProps(
                          column.getSortByToggleProps()
                        )}
                      >
                        <span className={classes.span}>
                          {column.render('Header')}
                          {column.isSorted ? (
                            getColumnOrder(column.isSortedDesc)
                          ) : (
                            <BsArrowDownUp size={20} />
                          )}
                        </span>
                        <div>
                          {column.canFilter ? column.render('Filter') : null}
                        </div>
                      </th>
                    ))}
                  </tr>
                ))}
              </thead>
              <tbody {...getTableBodyProps()}>
                {page.map((row) => {
                  prepareRow(row);
                  return (
                    <tr {...row.getRowProps()}>
                      {row.cells.map((cell) => {
                        return (
                          <td {...cell.getCellProps()}>
                            {cell.render('Cell')}
                          </td>
                        );
                      })}
                    </tr>
                  );
                })}
              </tbody>
            </table>
            <div className={classes.pagination}>
              <span>
                Page{[' ']}
                <strong>
                  {pageIndex + 1} of {pageOptions.length}
                </strong>{' '}
              </span>
              <span>
                | Go to page:{' '}
                <input
                  type='number'
                  defaultValue={pageIndex + 1}
                  onChange={(e) => {
                    const pageNumber = e.target.value
                      ? Number(e.target.value) - 1
                      : 0;
                    gotoPage(pageNumber);
                  }}
                  style={{ width: '50px' }}
                ></input>
              </span>
              <select
                className={classes.pageSize}
                value={pageSize}
                onChange={(e) => setPageSize(Number(e.target.value))}
              >
                {[25, 50, 100].map((showPageSize) => (
                  <option key={showPageSize} value={showPageSize}>
                    Show {showPageSize}
                  </option>
                ))}
              </select>
              <button
                className={classes.paginationBtn}
                onClick={() => gotoPage(0)}
                disabled={!canPreviousPage}
              >
                <AiOutlineDoubleLeft />
              </button>
              <button
                className={classes.paginationBtn}
                onClick={() => previousPage()}
                disabled={!canPreviousPage}
              >
                <AiOutlineLeft />
              </button>
              <button
                className={classes.paginationBtn}
                onClick={() => nextPage()}
                disabled={!canNextPage}
              >
                <AiOutlineRight />
              </button>
              <button
                className={classes.paginationBtn}
                onClick={() => gotoPage(pageCount - 1)}
                disabled={!canNextPage}
              >
                <AiOutlineDoubleRight />
              </button>
            </div>
            <BackToTop />
          </div>
        </>
      )}
    </div>
  );
};
