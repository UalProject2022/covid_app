import { useState } from 'react';
import { useAsyncDebounce } from 'react-table';
import 'regenerator-runtime';

type FilterProps = {
  filter: string;
  setFilter: React.Dispatch<React.SetStateAction<string>>;
};

export default function TableGlobalFilter({ filter, setFilter }: FilterProps) {
  const [value, setValue] = useState(filter);

  const onChange = useAsyncDebounce((asyncValue) => {
    setFilter(asyncValue || undefined);
  }, 1000);

  return (
    <span>
      Search:{' '}
      <input
        value={value || ''}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
          setValue(e.target.value);
          onChange(e.target.value);
        }}
      ></input>
    </span>
  );
};
