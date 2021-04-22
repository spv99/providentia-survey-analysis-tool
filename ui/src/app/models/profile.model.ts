export class ClusterInfo {
    question: string;
    common_response: string[];
    common_response_count: number[];
}

export class Profile {
    clusterInfo: ClusterInfo[];
    respondents?: number;
}