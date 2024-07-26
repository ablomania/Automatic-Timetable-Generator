import { useState } from "react"
import { Text, TextInput, View } from "react-native"


export default function EditProfile({navigation}) {
    const [ userName, setUserName ] = useState("");
    const [ departmentId, setDepartmentId ] = useState("");
    const [ yearGroup, setYearGroup ] = useState("");
    const [ tableCode, setTableCode ] = useState("");

    return(
        <View>
            <Text>Name:</Text>
            <TextInput placeholder="type your name here"
                onChangeText={setUserName}
                value={userName}
            />
            <Text>Department</Text>
            
            <Text>yearGroup</Text>

            <Text>Teable code</Text>
        </View>
    )
}