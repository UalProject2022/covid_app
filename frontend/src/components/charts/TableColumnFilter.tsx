export default function TableColumnFilter({ column }: any) {
  const { filterValue, setFilter } = column;
  return (
    <span>
      Search:{' '}
      <input
        value={filterValue || ''}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
          setFilter(e.target.value)
        }
      ></input>
    </span>
  );
};
