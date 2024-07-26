import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet } from "react-native";
import AsyncStorage from '@react-native-async-storage/async-storage';
import { apiURL } from "../App";



export default function SignIn({ navigation }) {

    const [userName , setUserName] = useState("");
    const [code, setCode] = useState("");
    var table = {};
    var college = []
    var college_main;
    
    const handleContinue = async () => {
        try {
          async function fetchtable() {
            try {
              let tableUrl = apiURL + '/timetables/?code=' + code;
                let response = await fetch(tableUrl);
                if(!response.ok) {
                    throw new Error('Network response was not ok');
                }
                let result  = await response.json();
                table = result;
                college_main = table[0]['college_main'];
                let table_id = table[0]['id'];
                let collegeUrl = apiURL + '/colleges/?format=json&id=' + college_main;
                response = await fetch(collegeUrl);
                if(!response.ok) {
                    throw new Error('could not return college s1');
                }
                result  = await response.json();
                college = result;
                var college_name = college[0]['name']
                if(college_main && college_name) {
                  try{
                    await AsyncStorage.setItem('tableId', table_id.toString());
                    console.log("Saved table ID successfully")
                  }
                  catch (error) {
                      console.error('Error saving table ID:', error);
                  }
                  try{
                    await AsyncStorage.setItem('collegeId', college_main.toString());
                    console.log("Saved college ID successfully")
                  }
                  catch (error) {
                      console.error('Error saving college ID:', error);
                    }
                  try{
                    await AsyncStorage.setItem('userName', userName);
                    console.log("Saved userName successfully")
                  }
                  catch (error) {
                      console.error('Error saving user name:', error);
                  }
                  try{
                    await AsyncStorage.setItem('code', code);
                    console.log("Saved code successfully")
                  }
                  catch (error) {
                      console.error('Error saving code:', error);
                  }
                  try{
                    await AsyncStorage.setItem('collegeName', college_name);
                    console.log("Saved college name successfully")
                  }
                  catch (error) {
                    console.error('Error saving college name:', error);
                  }
                  finally{
                    navigation.navigate('SignInStack2')
                  }
                }                
            }
            catch(error) {
                console.error('Error fetching data: ', error);
            }
        }
          fetchtable()
        } catch (error) {
          console.error('Error saving data:', error);
        }
      };


      const getStoredData = async () => {
        try {
          const storedUserName = await AsyncStorage.getItem('userName');
        //   const storedYearGroup = await AsyncStorage.getItem('yearGroup');
        //   const storedCollege = await AsyncStorage.getItem('college');
        //   const storedDepartmentName = await AsyncStorage.getItem('departmentName');
          const storedcode = await AsyncStorage.getItem('code');
      
          console.log('Stored data:', {
            userName: storedUserName,
            // yearGroup: storedYearGroup,
            // college: storedCollege,
            // departmentName: storedDepartmentName,
            code: storedcode,
          });
        } catch (error) {
          console.error('Error retrieving data:', error);
        }
      };

  return (
    <View style={styles.container}>
        <Text style={styles.signInHeader}>Sign In</Text>
      <Text style={styles.label}>Name</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter your name"
        onChangeText={setUserName}
        value={userName}
      />
      <Text style={styles.label}>Code</Text>
      <TextInput
        style={styles.input}
        placeholder="Enter your code"
        keyboardType="numeric"
        onChangeText={setCode}
        value={code}
      />
      <Button title="Continue"
       onPress={handleContinue} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: "center",
    backgroundColor: "#f5f5f5", // Add a background color
  },
  label: {
    fontSize: 16,
    marginBottom: 10,
  },
  signInHeader: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 10,
    padding: 10,
    marginBottom: 20,
  },
});


