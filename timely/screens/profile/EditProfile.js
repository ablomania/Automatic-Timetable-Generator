import { useEffect, useState } from "react"
import { Text, TextInput, View, Button, StyleSheet, TouchableOpacity } from "react-native"
import Picker from "react-native-picker-select";
import { apiURL } from "../../App";
import MaxYearGroupPicker from "../../components/MaxYear";


export default function EditProfile({navigation}) {
    const [ userName, setUserName ] = useState("");
    const [ departmentId, setDepartmentId ] = useState("");
    const [ yearGroup, setYearGroup ] = useState("");
    const [ tableCode, setTableCode ] = useState("");
    const [ departments, setDepartments ] = useState([]);
    const [ collegeName, setCollegeName ] = useState("");
    async function fetchTable() {
        try{
            const response = await fetch(apiURL + '/timetables/?code=' + tableCode);
            if(!response) {
              console.log("Response is not ok");
            } else{
              var result = await response.json();
              var datatableId = result[0]['id'];
              var datacollegeId = result[0]['college_main'];
              console.log("ci1",datacollegeId);
            }
          } catch(error){
            console.log("Error fetching table: ", error);
          }
          finally{
            // saveResult(college_Id=datacollegeId, table_Id=datatableId, tableCode=code, userName=selectedUserName);
            // fetchCollege(collegeId=datacollegeId);
            fetchDepartments()
          }
    }
    async function fetchDepartments() {
        try{
            const departmentResponse = await fetch(apiURL + '/departments/?college_main_id='+ collegeId + '&format=json');
            if(!departmentResponse) {
                console.log("Error network");
            } else {
                const result = await departmentResponse.json();
                data = await result;
                setDepartments(data)
                
            }
        } catch(error) {
            console.warn("Error getting departments : ", error);
        }
    }
    async function saveResult(college_Id, table_Id, tableCode, user_Name) {
        console.log("Banku")
        if(college_Id && table_Id && tableCode && user_Name) {
          try{
            await AsyncStorage.setItem("collegeId", college_Id.toString());
            await AsyncStorage.setItem("tableId", table_Id.toString());
            await AsyncStorage.setItem("tableCode", tableCode.toString());
            await AsyncStorage.setItem("userName", user_Name);
            console.log("saved items successfully");
            return 1;
          }
          catch(error) {
            console.log("Could not save items", error);
          }
          
        }
        
      }
      async function fetchCollege(collegeId) {
        try{
            const response = await fetch(apiURL + '/colleges/?format=json&id=' + collegeId);
            if(!response) {
                console.log("Error ")
            } else{
                console.log("college");
                const result = await response.json();
                let tempCollegeName = result[0]['name'];
                setCollegeName(tempCollegeName)
                console.log("college");
                if (tempCollegeName){
                  await AsyncStorage.setItem("collegeName", tempCollegeName);
                }
                return 1
            }
        } catch(error) {
            console.log("Could not fetch college : ", error)
        }
      }
      console.log("dt", departments)
    return(
        <View>
          <View style={styles.item}>
            <Text>Name:</Text>
              <TextInput placeholder="type your name here"
                  onChangeText={setUserName}
                  value={userName}
                  style={styles.input}
              />
          </View>
          <View style={styles.item}>
            <Text>Table code</Text>
            <TextInput 
                placeholder="type table code here"
                value={tableCode}
                keyboardType="numeric"
                onChangeText={setTableCode}
                style={styles.input}
                />
          </View>
          <Button title="Search" onPress={() => fetchTable()} />
          <View style={styles.item}>
          <Text>Department</Text>
          {departments.length >= 1 ? (
                <Picker
                selectedValue={departmentId}
                onValueChange={(itemValue) => setDepartmentId(itemValue)}
            >
                {departments.map((dept) => (
                <Picker.Item key={dept.id} label={dept.name} value={dept.id} />
                ))}
            </Picker>
            ) : (
                <Text>None</Text>
            )}
          </View>        
            <Text>yearGroup</Text>
            {/* {departmentId.length > 0 ? (
            <MaxYearGroupPicker departments={departments} selectedDepartment={departmentId}/>
            ) : (
                <Text>None</Text>
            )} */}
            <View style={styles.item}>
              <Text>College</Text>
              <Text>{collegeName}</Text>
            </View>
            <TouchableOpacity>
              <Text>Save</Text>
            </TouchableOpacity>
            <Button title="save" />
        </View>
    )
}

const styles = StyleSheet.create({
  item: {
    borderRadius: 10,
    backgroundColor: '#fafafa',
    padding: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: 'grey',
    borderRadius: 10,
    height: 50,
  },
})