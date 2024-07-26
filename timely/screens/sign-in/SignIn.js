import { useEffect, useState } from 'react'
import { View, Text, TextInput, Button, StyleSheet } from 'react-native'
import { apiURL } from '../../App';
import AsyncStorage from '@react-native-async-storage/async-storage';

const SignIn = ({navigation}) => {
    const [ selectedUserName, setSelectedUserName ] = useState('');
    const [ code, setCode ] = useState('');

    async function handleButton() {
      await fetchTable();
      navigation.navigate("SignInSec");
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
        saveResult(college_Id=datacollegeId, table_Id=datatableId, tableCode=code, userName=selectedUserName);
        fetchCollege(collegeId=datacollegeId);
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
        <View style={styles.container}>
        <Text>Name</Text>
        <TextInput
          style={styles.textInput}
          onChangeText={setSelectedUserName}
          value={selectedUserName}
        />
        <Text>Code</Text>
        <TextInput
          style={styles.textInput}
          onChangeText={setCode}
          value={code}
          keyboardType='numeric'
        />
        <Button style={styles.button} title='Continue'
          onPress={() => {handleButton()}}
        />
      </View>
    )
}
export default SignIn;

const styles = StyleSheet.create({
    container: {
      flex: 1,
      padding: 16,
      backgroundColor: '#F5F5F5',
      justifyContent: 'center',
    },
    textInput: {
      fontSize: 16,
      borderWidth: 1,
      borderColor: '#CCCCCC',
      padding: 8,
      marginBottom: 16,
      borderRadius: 4,
      backgroundColor: '#FFFFFF',
    },
    button: {
      backgroundColor: '#007AFF',
      padding: 12,
      borderRadius: 4,
      alignItems: 'center',
    },
    buttonText: {
      color: '#FFFFFF',
      fontSize: 18,
      fontWeight: 'bold',
    },
  });