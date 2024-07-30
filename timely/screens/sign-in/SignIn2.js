import AsyncStorage from "@react-native-async-storage/async-storage";
import { useEffect, useState } from "react";
import { Text, View, StyleSheet, Button, SafeAreaView, TouchableOpacity } from "react-native";
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
    const [ noError, setNoError ] = useState(0);

    useEffect(()=> {
        getStoredItems();
    },[])

    async function getStoredItems() {
        try{
            let storedcollegeId = await AsyncStorage.getItem("collegeId");
            let storedCollegeName = await AsyncStorage.getItem("collegeName")
            if(storedCollegeName.length && storedcollegeId.length) {
                setCollegeName(storedCollegeName);
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
        const yearGroup = await AsyncStorage.getItem("yearGroup")
        if(yearGroup > 0) {
            await navigation.navigate("HomeTabs1");
        }
        else {
            alert("Please choose a year group to continue");
        }
        
    }
    console.log('cn', collegeName);
    if(collegeName.length >= 1){
        return(
            <View style={styles.container}>
                <View style={styles.subContainer2}>
                    <Text style={styles.heading}>One more step..</Text>
                </View>
                <View style= {styles.subContainer}>
                    
                    <Text style={styles.label}>College</Text>
                    <Text style={styles.value}>{collegeName}</Text>
                    <Text style={styles.label}>Department</Text>
                    <Picker
                        style={styles.picker}
                        selectedValue={departmentId}
                        placeholder="Select a Department"
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
                    <TouchableOpacity 
                        style={styles.button}
                        onPress={()=> {handleButton()}}
                        >
                        <Text style={{color:'#fff'}}>Finish</Text>
                    </TouchableOpacity>
                </View>
                
            </View>
    
        )
    } else {
        return(
            <SafeAreaView style={{ justifyContent: 'center', padding: 20}}>
                <View style={{justifyContent: 'center', marginVertical: 250}}>
                <Text style={{fontWeight: 'bold', padding: 20, paddingBottom: 60}}>
                    Table does not exist
                </Text>
                <Text style={{color: 'grey'}}>Please make sure that you entered the correct code</Text>
                <TouchableOpacity onPress={() => navigation.navigate("SignInFirst")}>
                    <Text>Go Back</Text>
                </TouchableOpacity>
                </View>
                
            </SafeAreaView>
        )
    }
    
}

  
const styles = StyleSheet.create({
    subContainer: {
        backgroundColor: '#fff',
        padding: 16,
        borderRadius: 20,
        height: 500,
      },
    subContainer2: {
        backgroundColor: '#1976d2',
        height: 350,
        margin: 0,
        justifyContent: 'flex-end'
      },
    container: {
        flex: 1,
        backgroundColor: '#1976d2',
        justifyContent: 'center',
    },
    heading: {
        fontSize: 24,
        fontWeight: 'bold',
        textAlign: 'center',
        marginBottom: 16,
        marginBottom: 40,
        color: '#fff',
    },
    label: {
        fontWeight: 'bold',
        marginBottom: 8,
    },
    value: {
        marginBottom: 30,
    },
    picker: {
        borderWidth: 1,
        borderColor: '#ccc',
        borderRadius: 8,
        marginBottom: 16,
        padding: 8,
        backgroundColor: '#eceff1',
        borderRadius: 10,
        marginBottom: 30,
    },
    button: {
        backgroundColor: '#1976d2',
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: 5,
        height: 40,
        marginTop: 30,
    }
});
