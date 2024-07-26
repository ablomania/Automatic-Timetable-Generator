import React, { useEffect, useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Picker } from '@react-native-picker/picker';
import MaxYearGroupPicker from "../components/max-year-group";
import { apiURL} from "../App";
import { useNavigation } from "@react-navigation/native";
import HomeTabs from "../navigation/tabs";


export default function SignIn2() {
    const navigation =useNavigation();
    const [collegeId, setCollegeId] = useState('')
    const [departments, setDepartments] = useState([]);
    const [collegeName, setcollegeName] = useState('');
    const [selectedDepartment, setSelectedDepartment] = useState(null);
    
    const getStoredData = async () => {
      try {
        const storedCollegeName = await AsyncStorage.getItem('collegeName');
        const storedCollegeId = await AsyncStorage.getItem('collegeId');
        setcollegeName(storedCollegeName);
        setCollegeId(storedCollegeId);
        fetchdepartments(id=storedCollegeId);
      } catch (error) {
        console.error('Error retrieving data:', error);
      }
    };
    async function fetchdepartments(id) {
      try {
          const response = await fetch(apiURL + ;
          if(!response.ok) {'/departments/?college_main_id='+ id + '&format=json')
              throw new Error('Network response was not ok');
          }
          const result  = await response.json();
          setDepartments(result);
      }
      catch(error) {
          console.error('Error fetching data: ', error);
      }
    }
    useEffect(() => {
      getStoredData();
    },[])

    const handleFinish = async () => {
        try {
          // Save data to AsyncStorage
            await AsyncStorage.setItem('departmentId', toString(selectedDepartment));
          // Navigate to the next screen or perform any other action
          console.log('Dept saved successfully!');
          navigateToHome();
        } catch (error) {
            console.error('Error saving dept:', error);
        }
    };
    const navigateToHome = () => {
      return <HomeTabs />
    };
    console.log("sd",selectedDepartment)
    return (
          <View style={styles.container}>
            <Text style={styles.signInHeader}>Sign In</Text>
            <Text>College</Text>
            <Text>{collegeName}</Text>
            <Text style={styles.label}>Departments</Text>
            <Picker 
              selectedValue={selectedDepartment}
              onValueChange={(itemValue) => setSelectedDepartment(itemValue)}
            >
              {departments.map((dept) => (
                <Picker.Item key={dept.id}
                  label={dept.name}
                  value={dept.id}
                />
              ))}
            </Picker> 

            <Text style={styles.label}>Year Group</Text>
            <MaxYearGroupPicker selectedDepartment={selectedDepartment} departments={departments} />
            <Button title="Continue"
            onPress={() => handleFinish()} />
        </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#f9f9f9',
  },
  signInHeader: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 16,
  },
  label: {
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 16,
  },
  collegeName: {
    fontSize: 18,
    marginBottom: 16,
  },
});