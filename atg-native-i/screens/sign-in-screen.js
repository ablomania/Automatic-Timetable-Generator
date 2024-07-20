import { useState } from "react";
import { SafeAreaView, TextInput, View } from "react-native";

export default function SignIn() {
    const [userName , setUserName] = useState("");
    const [yearGroup, setYearGroup] = useState("");
    const [college, setCollege] = useState("");
    const [departmentName, setDepartmentName] = useState("");
    View
    return(
        <SafeAreaView>
            <View>
                <Text>Name</Text>
                <TextInput />
                <Text>Year Group</Text>
                <TextInput />
                <Text>College</Text>
                <TextInput />
                <Text>Department</Text>
                <TextInput />

            </View>
        </SafeAreaView>
    )

}