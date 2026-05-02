class InsightService:

    def summarize(self, df):
        return df.head(20).to_string(index=False)
