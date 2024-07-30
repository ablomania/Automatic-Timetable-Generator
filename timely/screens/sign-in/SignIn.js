import { useEffect, useState } from 'react'
import { View, Text, TextInput, Button, StyleSheet, SafeAreaView, TouchableOpacity } from 'react-native'
import { apiURL } from '../../App';
import AsyncStorage from '@react-native-async-storage/async-storage';

const SignIn = ({navigation}) => {
    const [ selectedUserName, setSelectedUserName ] = useState('');
    const [ code, setCode ] = useState('');
  
    async function handleButton() {
      if(selectedUserName.length > 0 && code.length > 0) {
        await fetchTable();
      }else {
        console.log("no input")
      }
    }

    async function fetchTable(){
      try{
        const response = await fetch(apiURL + '/timetables/?code=' + code);
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
        if(datacollegeId > 0) {
          saveResult(college_Id=datacollegeId, table_Id=datatableId, tableCode=code, userName=selectedUserName);
          fetchCollege(collegeId=datacollegeId);
          navigation.navigate("SignInSec");
        } else {
          alert("timetable not found!")
        }
      }
    }
    async function saveResult(college_Id, table_Id, tableCode, user_Name) {
      console.log('cd',user_Name)
      if(college_Id>0 && table_Id>0 && tableCode && user_Name) {
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
        
      }else {
        console.log("Could not save items")
      }
      
    }
    async function fetchCollege(collegeId) {
      console.log(collegeId)
     
      try{
        const response = await fetch(apiURL + '/colleges/?format=json&id=' + collegeId);
        if(!response) {
            console.log("Error ")
        } else{
            console.log("college");
            const result = await response.json();
            let tempCollegeName = result[0]['name'];
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

    return(
      <SafeAreaView style={styles.container}>
          <View style={styles.subContainer2}>
            <Text style={styles.heading}>New to timely?</Text>
          </View>
          
        <View style={styles.subContainer}>
          <Text style={styles.signin}>Sign In</Text>
          <Text style={styles.label}>Name</Text>
          <TextInput
            style={styles.textInput}
            onChangeText={setSelectedUserName}
            value={selectedUserName} 
          />
          <Text style={styles.label}>Code</Text>
          <TextInput
            style={styles.textInput}
            onChangeText={setCode}
            value={code}
            keyboardType='numeric'
          />
          <TouchableOpacity
          style={styles.button}
          onPress={() => handleButton()}
          >
          <Text style={{color: '#fff'}}>Continue</Text>
          </TouchableOpacity>
        </View>
    </SafeAreaView>
    )
}
export default SignIn;


const styles = StyleSheet.create({
    subContainer: {
      backgroundColor: '#fff',
      padding: 16,
      borderRadius: 20,
      height: 450,
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
      fontSize: 28,
      fontWeight: 'bold',
      textAlign: 'center',
      marginBottom: 70,
      color: '#fff',
    },
    label: {
        fontWeight: 'bold', // Make labels bold
        marginBottom: 8,
    },
    textInput: {
        borderWidth: 1,
        borderColor: '#ccc',
        borderRadius: 8, // Add border radius to text input fields
        padding: 8,
        marginBottom: 16,
    },
    button: {
        borderRadius: 8,
        alignItems: 'center',
        backgroundColor: '#1976d2',
        height: 40,
        justifyContent: 'center',
        width: 325,
        alignSelf: 'center'
    },
    signin: {
      fontWeight: 'bold',
      fontSize:20,
      marginBottom: 30
    }
});


