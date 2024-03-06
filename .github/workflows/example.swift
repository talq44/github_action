//
//  example.swift
//  
//
//  Created by 박창규 on 3/6/24.
//

import Foundation

// 명령행 인수로부터 값을 받아 출력
if CommandLine.arguments.count > 1 {
    let value = CommandLine.arguments[1]
    print("Received value:", value)
} else {
    print("No value received")
}

// 출력
print("Hello from Swift!")
