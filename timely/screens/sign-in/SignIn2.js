import AsyncStorage from "@react-native-async-storage/async-storage";
import { useEffect, useState } from "react";
import { Text, View, StyleSheet, Button } from "react-native";
import { apiURL } from "../../App";
import { Picker } from "@react-native-picker/picker";
import MaxYearGroupPicker from "../../components/MaxYear";
import { HomeTabs } from "../../navigation/tab";
import { HomeStack } from "../../navigation/stack";

export default function SignIn2({navigation}) {
    const [ departmentId, setDepartmentId ] = useState("");
    const [ yearGroup, setYearGroup ] = useState("");
    const [ collegeName, setCollegeName ] = useState("");
    const [ departmentList, setDepartmentList ] = useState([]);

    useEffect(()=> {
        getStoredItems();
    },[])

    async function getStoredItems() {
        try{
            let storedcollegeId = await AsyncStorage.getItem("collegeId");
            let storedCollegeName = await AsyncStorage.getItem("collegeName")
            if(storedCollegeName.length && storedcollegeId.length) {
                setCollegeName(storedCollegeName);
                console.log("ci", storedcollegeId)
                console.log("nc", storedCollegeName);
                fetchDepartments(collegeId=storedcollegeId);
            }
                
        }
        catch(error) {
            console.log("Error getting stored collegeId :", error);
        }
    }
    async function fetchDepartments(collegeId) {
        try{
            const response = await fetch(apiURL + '/departments/?college_main_id='+ collegeId + '&format=json');
            if(!response) {
                console.log("Network issue");
            } else{
                result = await response.json();
                setDepartmentList(result);
            }
        }
        catch(error) {
            console.log("Error getting departments : ", error);
        }
    }
    async function handleButton() {
        await AsyncStorage.setItem("departmentId", departmentId.toString());
        await navigation.navigate("HomeTabs1");
    }
    
    return(
        <View style={styles.container}>
            <Text style={styles.heading}>Details</Text>
            <Text style={styles.label}>College</Text>
            <Text style={styles.value}>{collegeName}</Text>
            <Text style={styles.label}>Department</Text>
            <Picker
                style={styles.picker}
                selectedValue={departmentId}
                onValueChange={(itemValue) => setDepartmentId(itemValue)}
            >
                {departmentList.map((dept) => (
                <Picker.Item key={dept.id} label={dept.name} value={dept.id} />
                ))}
            </Picker>
            <Text style={styles.label}>Year Group</Text>
            <MaxYearGroupPicker
                style={styles.picker}
                selectedDepartment={departmentId}
                departments={departmentList}
            />
            <Button title="Continue" onPress={()=> {handleButton()}} />
        </View>

    )
}

const styles = StyleSheet.create({
    container: {
    justifyContent: "center",
    padding: 16,
    paddingTop: 100,
    backgroundColor: '#f9f9f9',
    },
    heading: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 8,
    },
    label: {
    fontSize: 16,
    marginBottom: 4,
    },
    value: {
    fontSize: 16,
    color: '#333',
    marginBottom: 12,
    },
    picker: {
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 4,
    marginBottom: 12,
    },
  });
  