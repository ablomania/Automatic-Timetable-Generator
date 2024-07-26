import AsyncStorage from "@react-native-async-storage/async-storage";
import { useState } from "react";
import RNPickerSelect from 'react-native-picker-select';


const MaxYearGroupPicker = ({departments, selectedDepartment }) => {
    const [selectedYearGroup, setSelectedYearGroup] = useState(null);
    // Get the max_year_group of the selected department
    const maxYearGroup = departments.find((dept) => dept.id === selectedDepartment)?.max_yg;
    // Generate an array of numbers from 1 to max_year_group
    const yearGroupOptions = Array.from({ length: maxYearGroup}, (_, index) => ({
      label: `${index + 1}`,
      value: index + 1,
    }));
    const Finish = async () => {
        try {
          // Save data to AsyncStorage
          console.log("sy", selectedYearGroup)
            await AsyncStorage.setItem('yearGroup', toString(selectedYearGroup));            
          // Navigate to the next screen or perform any other action
            console.log('year group saved successfully!');
        } catch (error) {
            console.error('Error saving year group:', error);
        }
    };
    Finish();
    return (
      <RNPickerSelect
        onValueChange={(value) => setSelectedYearGroup(value)}
        items={yearGroupOptions}
      />
    );
  };
  
export default MaxYearGroupPicker;