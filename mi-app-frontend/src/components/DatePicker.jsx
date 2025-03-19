import { useState } from 'react';
import 'react-datepicker/dist/react-datepicker.css';
import DatePicker from 'react-datepicker';

export default function CustomDatePicker({ selectedDate, onChange }) {
  const [startDate, setStartDate] = useState(
    selectedDate ? new Date(selectedDate) : null
  );

  const handleChange = (date) => {
    setStartDate(date);
    onChange(date);
  };

  return (
    <DatePicker
      selected={startDate}
      onChange={handleChange}
      dateFormat="dd/MM/yyyy"
      showYearDropdown
      dropdownMode="select"
      maxDate={new Date()}
      placeholderText="Seleccione su fecha de nacimiento"
    />
  );
}